#!/bin/bash
if [ "$(id -u)" -ne 0 ]; then
    exec sudo -E "$0" "$@"
fi
cd "$(dirname "$0")" || exit 1
python3 main.py
