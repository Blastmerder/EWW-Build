#!/usr/bin/env python3
import subprocess
import sys
import os
from listener import listener

# I use mpd, so i will use base path. change to your directory with conf file for mpd.

def get_path_to_album():
    path = subprocess.check_output("./scripts/get_path_to_music_file.sh").decode('utf-8').split('\n')

    if path[1] == '':
        print("'./images/album.svg'")
    else:
        HOME = subprocess.check_output(['pwd'], text=True).split('.')[0]
        audio_path = f'{path[0].replace('~', HOME)}/{path[1]}'.replace('//', '/')
        
        out_put = './cache/media/album.png'

        command = [
            'ffmpeg',
            '-y',
            '-i',
            audio_path,
            '-an',
            '-vcodec',
            'copy',
            out_put,
            '-loglevel',
            'quiet'
        ]
        subprocess.run(command)
        print(f"'{out_put}'")


match sys.argv[1]:
    case '--image':
        listener(get_path_to_album, 'mpc idle player'.split(' '))
    
    case '--track-title':
        listener(get_path_to_album, 'mpc idle player'.split(' '))
