#!/usr/bin/env python3

import subprocess
from listener import listener
from time import sleep

images = {
    '$empty-select': "'images/workspaces/full/Select.svg'",
    '$empty-deselect': "'images/workspaces/empty/Deselect.svg'",
    '$full-select': "'images/workspaces/full/Select.svg'",
    '$full-deselect': "'images/workspaces/empty/Select.svg'"
}

def get_workspaces():
    try:
        command = 'bspc query -D -d .occupied --names'.split(' ')
        out_put = subprocess.check_output(command).decode('utf-8').split('\n')
        del out_put[-1]

        command = 'bspc query -D --names'.split(' ')
        out_put1 = subprocess.check_output(command).decode('utf-8').split('\n')
        del out_put1[-1]

        command = 'bspc query -D -d focused --names'.split(' ')
        selected_desktop = subprocess.check_output(command).decode('utf-8')
        icons = ['$empty-deselect'] * len(out_put1)

        for desk in out_put:
            icons[out_put1.index(desk)] = '$full-deselect'

        icons[out_put1.index(selected_desktop.replace('\n', ''))] = f'{icons[out_put1.index(selected_desktop.replace('\n', ''))].split('-')[0]}-select'

        result = []

        for i in range(len(out_put1)):
            result.append(f'(button :onclick "bspc desktop -f {i+1}" :class "button" :style "background-image: url({images[icons[i]]}); padding-right: 5px;") ')

        print(f'(box :class "workspaces_bar" :orientation "h" :space-evenly false :haligh "start" {"".join(result)})')
        return f'(box :class "workspaces_bar" :orientation "h" :space-evenly false :haligh "start" {"".join(result)})'
    except:
        sleep(1)
        get_workspaces()

listener(get_workspaces, "bspc subscribe desktop node_transfer".split(' '))