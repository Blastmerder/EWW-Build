#!/usr/bin/env python3
import subprocess
import sys


volume = subprocess.check_output("wpctl get-volume @DEFAULT_AUDIO_SINK@".split(' ')).decode('utf-8')
volume = int(float(volume.replace('\n', '').split(' ')[-1])*100)


match sys.argv[1]:
    case '--value':
        print(volume)
    case '--icon':
        if 0 < volume < 30:
            print("'images/volume/less 30.svg'")
        if 80 > volume >= 30:
            print("'images/volume/more 30.svg'")
        if volume >= 80:
            print("'images/volume/more 80.svg'")
        if volume == 0:
            print("'images/volume/mute.svg'")