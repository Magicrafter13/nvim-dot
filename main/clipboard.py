#!/usr/bin/python3
"""Configure user's clipboard."""

import json
import os

from utils import read_file  # pylint: disable=import-error

config = json.loads(read_file(("config.json")))

base = json.loads(read_file(("configs/base.json")))

if __name__ == "__main__":
    # Read config files
    selected_base = (
        base[config["base"]]
        if config and config["base"] in base
        else {})

    # Clipboard
    print("\033[1;32mSetting up Clipboard Provider...\033[0m")
    # if config doesn't specify, then ask
    if "clipboard" not in selected_base:
        print(
            "Select System Environment"
            "\n\t0) None\n\t1) KDE\n\t2) Xfce\n\t3) Termux")
        selected_base['clipboard'] = int(input())
    if selected_base['clipboard'] == 0:
        print("Continuing without custom clipboard provider.")
        os.system('rm -f nvim/lua/clipboard.lua')
    elif selected_base['clipboard'] == 1:
        print("Neovim will use Klipper to Copy/Paste.")
        os.system('cp main/kde_clipboard.lua nvim/lua/clipboard.lua')
        home = os.path.expanduser('~')
        if (
            os.path.exists(home + '/.local/bin')
            and os.path.isdir(home + '/.local/bin')
            and not os.path.exists(home + '/.local/bin/klipperCopy')
        ):
            os.system(f'cp main/klipperCopy {home}/.local/bin/')
    elif selected_base['clipboard'] == 2:
        print("Xfce4 clipboard should work with Neovim out-of-the-box.")
        os.system('rm -f nvim/lua/clipboard.lua')
    elif selected_base['clipboard'] == 3:
        print(
            "Neovim will use Termux API. Make sure to install the "
            "package, and the corresponding Android package!")
        os.system('cp main/termux_clipboard.lua nvim/lua/clipboard.lua')
    elif selected_base['clipboard'] == 4:
        print("Wayland clipboard is supported via wl-clipboard and wayclip in Neovim out-of-the-box.")
        os.system('rm -f nvim/lua/clipboard.lua')
    else:
        print("Invalid environment - continuing with setup.")
