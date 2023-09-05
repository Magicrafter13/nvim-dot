#!/usr/bin/python3
"""Construct nvim/lua/colorscheme.lua from
config.json, .plugins and plugins.json"""

import json

from utils import read_file, write_file, load_plugins  # noqa: E501  pylint: disable=import-error

config = json.loads(read_file("config.json"))
installed = json.loads(read_file(".plugins"))["plugins"]
plugins = load_plugins()


def set_colorscheme(name):
    """Set the colorscheme for NeoVim and lightline"""
    data = f'vim.cmd("colorscheme {name}")'
    if "lightline" in installed:
        data += f'''local old_lightline = vim.g.lightline or {{}}
old_lightline.colorscheme = "{name}"
vim.g.lightline = old_lightline
vim.call("lightline#enable")'''
    write_file("nvim/lua/colorscheme.lua", f"{data}\n")


if __name__ == "__main__":
    print("\033[1;32mSetting colorscheme\033[0m")
    schemes_installed = dict(
        (name, plugins[name])
        for name in installed
        if name in plugins and "colorscheme" in plugins[name]["attributes"])
    for k, v in schemes_installed.items():
        if "colorscheme" not in v:
            v["colorscheme"] = k
    if len(schemes_installed) == 0:
        print("No colorschemes were installed! :(")
        write_file("nvim/lua/colorscheme.lua", "")
    elif len(schemes_installed) == 1:
        set_colorscheme(list(schemes_installed.values())[0]["colorscheme"])
    elif len(config["colors"]) > 0:
        set_colorscheme(schemes_installed[config["colors"][0]]["colorscheme"])
    else:
        print(
            "More than 1 colorscheme installed, please select one to use "
            "by default:")
        for _name in schemes_installed:
            print(f"\t{_name} - {schemes_installed[_name]['comment']}")
        selection = input()
        if selection in schemes_installed:
            set_colorscheme(schemes_installed[selection]["colorscheme"])
        else:
            write_file("nvim/lua/colorscheme.lua", "")
