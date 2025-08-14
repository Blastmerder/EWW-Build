#!/usr/bin/env python3
import subprocess


cava = subprocess.check_output('./scripts/get_current_vol.sh'.split(' ')).decode('utf-8')
cava = ''.join(str(cava).replace('\n', '').split(';')[:-1])

print(int(cava) > 0)
