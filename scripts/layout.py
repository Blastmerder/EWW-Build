#!/usr/bin/env python3
import subprocess
import sys


layouts = subprocess.check_output("setxkbmap -query".split(' ')).decode('utf-8').split('layout:     ')[1].split('options:')[0].replace('\n', '').split(',')
# xset -q | grep LED | awk '{ print $10 }')


number_of_layout = subprocess.check_output("xset -q".split(' ')).decode('utf-8').split('LED mask:  ')[1].split('XKB indicators:')[0].replace('\n', '').replace(' ', '')


if sys.argv[1] == '--layout':
    print(layouts[int(number_of_layout[-4])])
if sys.argv[1] == '--caps':
    print(str(number_of_layout[-1]=='1').lower())
