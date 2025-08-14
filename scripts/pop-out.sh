pop() {
LOCK_FILE_SONG="$HOME/.cache/eww-$1.lock"

run() {
    eww open $1
}

# Open widgets
if [[ ! -f "$LOCK_FILE_SONG" ]]; then
    touch "$LOCK_FILE_SONG"
    run $1
else
    eww close $1
    rm "$LOCK_FILE_SONG" && echo "closed"
fi
}

pop $1