#!/bin/bash
set -e
version="v_$(date +%Y%m%d)"
pyinstaller --onefile --windowed --icon assets/GameSpace.ico -n game_space game_space.py
zip -r "Game_Space_EXE_${version}.zip" dist/game_space assets
