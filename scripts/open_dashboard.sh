pop() {
    LOCK_FILE_SONG="$HOME/.cache/eww-dashboard.lock"

    # Open widgets
    if [[ ! -f "$LOCK_FILE_SONG" ]]; then
        touch "$LOCK_FILE_SONG"
        eww open-many background \
                        music_win_dash
    else
        eww close background \
                  music_win_dash
        rm "$LOCK_FILE_SONG" && echo "closed"
    fi
}

pop