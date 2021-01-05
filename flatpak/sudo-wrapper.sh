#!/bin/sh

command="$0"
sudo_command=${command#"/app/bin/"}
flatpak-spawn --host --clear-env "$sudo_command" "$@"
