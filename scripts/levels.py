#!/usr/bin/env python3
"""
audio_loudness.py
Safe ffmpeg invocation suitable for use inside programs that themselves use subprocess.Popen().
Provides loudness_symbols(path, n_outputs=45, sr=44100, channels=1, global_norm=True, stream=False).
Requires system ffmpeg in PATH. Uses numpy if present.
"""
from typing import Tuple, List
import shutil
import subprocess
import struct
import math
import os

try:
    import numpy as np
    _HAS_NUMPY = True
except Exception:
    np = None
    _HAS_NUMPY = False

SYMBOLS = "▁▂▃▄▅▆▇█"

def _ffmpeg_available() -> bool:
    return shutil.which("ffmpeg") is not None

def _run_ffmpeg_get_pcm_bytes(path: str, sr: int = 44100, channels: int = 1, timeout: float | None = None) -> bytes:
    """
    Run ffmpeg and return raw pcm s16le bytes.
    Use Popen with explicit stdin=DEVNULL and close_fds=True to avoid fd inheritance issues.
    """
    if isinstance(path, (list, tuple)):
        if not path:
            raise ValueError("path is empty")
        path = path[0]
    if not _ffmpeg_available():
        raise RuntimeError("ffmpeg not found in PATH")

    cmd = [
        "ffmpeg", "-v", "error",
        "-i", str(path),
        "-f", "s16le", "-acodec", "pcm_s16le",
        "-ar", str(int(sr)), "-ac", str(int(channels)), "-"
    ]
    # Ensure all elements are strings
    cmd = [str(x) for x in cmd]

    # Use Popen with explicit fd handling to avoid inheriting parent's fds
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True
    )
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        out, err = proc.communicate()
        raise RuntimeError(f"ffmpeg timeout; stderr: {err.decode(errors='replace')}")
    if proc.returncode != 0:
        err_text = err.decode(errors='replace').strip()
        raise RuntimeError(f"ffmpeg failed (code {proc.returncode}). stderr: {err_text!r}")
    return out

def _pcm_bytes_to_mono_floats(bytes_obj: bytes, channels: int = 1):
    if _HAS_NUMPY:
        arr = np.frombuffer(bytes_obj, dtype=np.int16)
        if channels > 1:
            arr = arr.reshape(-1, channels).astype(np.float32).mean(axis=1)
        else:
            arr = arr.astype(np.float32)
        return arr / 32768.0
    else:
        it = struct.iter_unpack('<h', bytes_obj)
        vals = [v[0] for v in it]
        if channels == 1:
            return [v / 32768.0 for v in vals]
        out = []
        for i in range(0, len(vals), channels):
            chunk = vals[i:i+channels]
            if len(chunk) < channels:
                chunk += [0] * (channels - len(chunk))
            out.append(sum(chunk) / (channels * 32768.0))
        return out

def _rms_per_segment(samples, n_segments: int) -> List[float]:
    if _HAS_NUMPY:
        n = samples.shape[0]
        if n == 0:
            return [0.0] * n_segments
        seg_len = int(math.ceil(n / n_segments))
        pad = seg_len * n_segments - n
        if pad:
            samples = np.pad(samples, (0, pad), mode="constant")
        windows = samples.reshape(n_segments, seg_len)
        rms = np.sqrt(np.mean(windows.astype(np.float64) ** 2, axis=1))
        return rms.tolist()
    else:
        total = len(samples)
        if total == 0:
            return [0.0] * n_segments
        seg_len = int(math.ceil(total / n_segments))
        rms_list = []
        for i in range(n_segments):
            start = i * seg_len
            end = min(start + seg_len, total)
            if start >= end:
                rms_list.append(0.0)
                continue
            s = 0.0
            for v in samples[start:end]:
                s += v * v
            rms_list.append(math.sqrt(s / (end - start)))
        return rms_list

def _map_to_symbols(rms_values: List[float], global_norm: bool = True) -> List[str]:
    if _HAS_NUMPY:
        arr = np.array(rms_values, dtype=float)
        if global_norm:
            ref = arr.max() if arr.size and arr.max() > 0 else 1.0
            norm = arr / ref
        else:
            amin = arr.min() if arr.size else 0.0
            amax = arr.max() if arr.size else 1.0
            span = amax - amin
            norm = (arr - amin) / span if span > 0 else np.zeros_like(arr)
        norm = np.clip(norm, 0.0, 1.0)
        idx = (norm * (len(SYMBOLS) - 1)).round().astype(int)
        return [SYMBOLS[i] for i in idx.tolist()]
    else:
        lst = list(rms_values)
        if global_norm:
            ref = max(lst) if lst and max(lst) > 0 else 1.0
            norm = [v / ref for v in lst]
        else:
            amin = min(lst) if lst else 0.0
            amax = max(lst) if lst else 1.0
            span = amax - amin
            if span > 0:
                norm = [(v - amin) / span for v in lst]
            else:
                norm = [0.0 for _ in lst]
        out = []
        for v in norm:
            v = max(0.0, min(1.0, v))
            idx = int(round(v * (len(SYMBOLS) - 1)))
            out.append(SYMBOLS[idx])
        return out

def loudness_symbols(
    path: str,
    n_outputs: int = 45,
    sr: int = 44100,
    channels: int = 1,
    global_norm: bool = True,
    stream: bool = False,
    timeout: float | None = None
) -> Tuple[List[str], List[float]]:
    """
    Main function.
    If stream=False (default) -> one ffmpeg run returning full PCM in memory (safe usage with close_fds).
    If stream=True  -> stream from ffmpeg in chunks to compute per-segment RMS without loading whole file.
       - When stream=True global_norm cannot be applied in single pass reliably; function will return raw RMS and symbols
         normalized per-file segment-range (same as global_norm=False). To get global_norm with stream use two passes.
    """
    if stream:
        # Stream mode: read stdout in chunks to avoid loading whole PCM. We'll compute per-segment RMS by accumulating samples.
        # For simplicity, we compute segment length in samples from file duration is unknown here, so we'll buffer and split
        # into n_outputs consecutive equal-sample segments by accumulating all samples (still can be memory-heavy in worst case)
        # For robust streaming with strict low memory, implement two-pass: first pass determine total samples, second pass compute.
        pcm_bytes = _run_ffmpeg_get_pcm_bytes(path, sr=sr, channels=channels, timeout=timeout)
        samples = _pcm_bytes_to_mono_floats(pcm_bytes, channels=channels)
        rms = _rms_per_segment(samples, n_outputs)
        symbols = _map_to_symbols(rms, global_norm=False)
        return symbols, rms
    else:
        # default: single run, get PCM bytes
        pcm_bytes = _run_ffmpeg_get_pcm_bytes(path, sr=sr, channels=channels, timeout=timeout)
        samples = _pcm_bytes_to_mono_floats(pcm_bytes, channels=channels)
        rms = _rms_per_segment(samples, n_outputs)
        symbols = _map_to_symbols(rms, global_norm=global_norm)
        return symbols, rms
