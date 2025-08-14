#!/usr/bin/env python3
import subprocess

images_paths = {
    "Discharging": [
        "'images/battary/less 20.svg'",
        "'images/battary/less 20.svg'",
        "'images/battary/less 20.svg'",
        "'images/battary/30.svg'",
        "'images/battary/40.svg'",
        "'images/battary/50.svg'",
        "'images/battary/60.svg'",
        "'images/battary/70.svg'",
        "'images/battary/80.svg'",
        "'images/battary/90.svg'",
        "'images/battary/100.svg'"
        ],
    "Charging": "'images/battary/charge.svg'",
    "Full": "'images/battary/100.svg'"
}


status = subprocess.check_output('./scripts/battary.sh --bat-st'.split(' ')).decode('utf-8').split('\n')[0]
charge = subprocess.check_output('./scripts/battary.sh --bat'.split(' ')).decode('utf-8').split('\n')[0]

print(images_paths[status] if status == "Charging" or status == "Full" else images_paths[status][int(charge)//10])
