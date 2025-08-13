#!/bin/sh

./scripts/workspace.py
bspc subscribe desktop node_transfer | while read -r _ ; do
./scripts/workspace.py
done