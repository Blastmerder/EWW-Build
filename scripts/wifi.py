#!/usr/bin/env python3
import subprocess
import sys


PICTURES_PATHS = {
    "802-3-ethernet": "'images/wifi/lan.svg'",
    "disconnect": "'images/wifi/wifi_off.svg'",
    "802-11-wireless": "'images/wifi/wifi_3.svg'"
}

def get_image(connections):
    for connection in connections:
        if connection['ACTIVE'] == 'yes':
            print(PICTURES_PATHS[signals[0]['TYPE']])
            return
    print(PICTURES_PATHS["disconnect"])

def get_name_active(connections):
    for connection in connections:
        if connection['ACTIVE'] == 'yes':
            return connection['NAME']
    return None

# Get data about connections

data_list = 'NAME,ACTIVE,TYPE'

connections = [i.split(":") for i in subprocess.check_output(f"nmcli -t -f {data_list} connection show".split(' ')).decode('utf-8').split('\n')]
del connections[-1]

# Sort for camfort use

signals = [{(data_list).split(',')[i]: j[i] for i in range(len(j))} for j in connections]

for i in range(len(signals)):
    if signals[i]["TYPE"] == 'loopback':
        del signals[i]

# Return data

arg = sys.argv[1]

match arg:
    case "--icon":
        get_image(signals)
    case "--name-active":
        print(get_name_active(signals))       

