#!/usr/bin/env python3
import subprocess
import sys
import os
import shutil
from pathlib import Path

template_folder = Path('./templates/')
images_folder = Path('./images/')

shutil.rmtree(images_folder)

shutil.copytree(template_folder, images_folder, copy_function=shutil.copy2)

with open("./styles/Colors.scss", 'r', encoding='utf-8') as f:
    values = {i.split(':')[0].replace('$', '').replace(':', ''): i.split(':')[1] for i in f.read().replace(' ', '').replace('\n', '').split(';')[0:-1]}


for dirpath, dirnames, filenames in os.walk('./images/'):
    for name in filenames:
        if name.lower().endswith('.svg'):
            path = os.path.join(dirpath, name)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    text = f.read()
            except Exception as e:
                print(f'skip {path}: {e}', file=sys.stderr)
                continue

            for key in values.keys():
                if key in text:
                    new_text = text.replace(key, values[key])
                    try:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_text)
                    except Exception as e:
                        print(f"error writing {path}: {e}", file=sys.stderr)
                        continue
                        
                    print("updated", path)
