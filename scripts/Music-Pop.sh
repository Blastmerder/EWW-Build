music() {
LOCK_FILE_SONG="$HOME/.cache/eww-song.lock"

run() {
    eww open music_win 
}

# Open widgets
if [[ ! -f "$LOCK_FILE_SONG" ]]; then
    # eww -c $HOME/.config/eww/bar close system calendar
    touch "$LOCK_FILE_SONG"
    run && echo "ok good!"
else
    # eww -c $HOME/.config/eww/bar close music_win
    eww close music_win
    rm "$LOCK_FILE_SONG" && echo "closed"
fi
}

music