pop() {
    LOCK_FILE_SONG="$HOME/.cache/eww-dashboard.lock"

    run() {
        eww open 'dashboard'
    }

    # Open widgets
    if [[ ! -f "$LOCK_FILE_SONG" ]]; then
        touch "$LOCK_FILE_SONG"
        run 'dashboard'
    else
        eww close 'dashboard'
        rm "$LOCK_FILE_SONG" && echo "closed"
    fi
}

pop 'dashboard'