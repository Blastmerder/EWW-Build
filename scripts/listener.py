import subprocess
import sys
import os


def listener(child_func, proc: list):
    proc = subprocess.Popen(proc, stdout=subprocess.PIPE, text=True)
    child_func()
    try:
        while True:
            line = proc.stdout.readline()
            if line == "" and proc.poll() is None:
                break
            child_func()
    
            # proc = subprocess.Popen(proc, stdout=subprocess.PIPE, text=True)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            proc.terminate()
        except Exception:
            pass