#!/usr/bin/env python3
"""Construct the lazy-init.lua file (plugin loader)."""

import json
import sys

from utils import (  # pylint: disable=import-error
    read_file,
    write_file,
    load_plugins)

config = json.loads(read_file(("config.json")))

base = json.loads(read_file(("configs/base.json")))
env = json.loads(read_file(("configs/env.json")))
yes = json.loads(read_file(("configs/yes.json")))
programming = json.loads(read_file(("configs/programming.json")))
dev = json.loads(read_file(("configs/dev.json")))

plugins = load_plugins()
# A set would be better but I want the plugins added in the order we read
# them...
install = []


def set_plugins(plugin_list: list[str]):
    """Apply changes (like a mask) to an entry in the plugins dictionary."""
    for _p in plugin_list:
        if _p in plugins and _p not in install:
            install.append(_p)


def parse_config():
    """Read through user's config file and set plugin data accordingly."""
    # Base
    if len(config["base"]) > 0 and config["base"] in base:
        set_plugins(base[config["base"]]["plugins"])
    # Envs
    for environment in config["environment"]:
        if environment in env:
            set_plugins(env[environment])
    # Yes
    for pack in config["yes"]:
        if pack in yes:
            set_plugins(yes[pack])
    # Programming
    for pack in config["programming"]:
        if pack in programming:
            set_plugins(programming[pack])
    # Dev
    for pack in config["dev"]:
        if pack in dev:
            set_plugins(dev[pack])
    # Colors
    for color in config["colors"]:
        if "colorscheme" in plugins[color]["attributes"]:
            install.append(color)


_NL = "\n"


def check_valid_config():
    """Verify the user's config file is properly structured."""
    good_config = True
    if not isinstance(config["base"], str):
        print("Error in config file. Expected string for 'base'.")
        good_config = False
    if not isinstance(config["environment"], list):
        print("Error in config file. Expected [] list for 'environment'.")
        good_config = False
    if not isinstance(config["yes"], list):
        print("Error in config file. Expected [] list for 'yes'.")
        good_config = False
    if not isinstance(config["dev"], list):
        print("Error in config file. Expected [] list for 'dev'.")
        good_config = False
    if not isinstance(config["colors"], list):
        print("Error in config file. Expected [] list for 'colors'.")
        good_config = False
    return good_config


if __name__ == "__main__":
    print("\033[1;31mParsing config files\033[0m")
    if not check_valid_config():
        sys.exit(1)
    parse_config()

    print("\033[1;31mCaching list of Plugins\033[0m")
    # Clean bad entries from install list
    for idx, _plug in enumerate(install):
        if _plug not in plugins:
            print(f"No {_plug} entry found in plugins.json, skipping.")
            install.pop(idx)
    if "LSP" in config["programming"]:
        install.append("nvim-lspconfig")
        #install.append("fidget")
    write_file(".plugins", f'''{{"plugins":[{", ".join([
        f'"{name}"'
        for name in install])}]}}''')
