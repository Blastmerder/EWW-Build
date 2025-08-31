#!/bin/sh
path=echo awk -F"['\"]" '/^[[:space:]]*music_directory/ {print $2}' ~/.config/mpd/mpd.conf
file=echo mpc --format %file% current
echo "$path$file"