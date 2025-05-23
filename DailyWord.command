#!/bin/bash
            DIR="$(cd "$(dirname "$0")" && pwd)"
            osascript <<EOF
            tell application "Terminal"
                set newTab to do script "$DIR/bin/main_UserInput.app/Contents/MacOS/main_UserInput; exit"
                delay 1
                repeat while busy of window 1
                    delay 0.5
                end repeat
                close window 1
            end tell
            EOF
            