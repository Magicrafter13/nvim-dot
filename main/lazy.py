#!/usr/bin/python3
"""Construct nvim/lua/lazy-init.lua from .plugins and plugins.json"""

import json

from utils import read_file, write_file  # pylint: disable=import-error

installed = json.loads(read_file(".plugins"))["plugins"]
plugins = json.loads(read_file("plugins.json"))
for pid, val in list(plugins.items()):
    if pid.startswith("_"):
        plugins.pop(pid)
        continue
    if "attributes" not in val:
        val["attributes"] = []
    elif "colorscheme" in val["attributes"] and "colorscheme" not in val:
        val["colorscheme"] = pid


def construct_plugin_line(plugin: dict):
    """Construct a plugin spec line for use with lazy.nvim"""
    line = f'"{plugin["repo"]}",'
    if "params" in plugin:
        line = f'{{ {line} {", ".join(plugin["params"])} }},'
    elif "nerdtree" in plugin["attributes"]:
        line = f'{{ {line} dependencies = { "nerdtree" } }},'
    if "comment" in plugin:
        line += f" -- {plugin['comment']}"
    return line


NLTAB = "\n\t"

if __name__ == "__main__":
    print("\033[1;31mConstructing nvim/lua/lazy-init.lua\033[0m")
    write_file("nvim/lua/lazy-init.lua", f"""--
-- lazy.nvim
--
vim.g.mapleader = " "

require("lazy").setup({{
\t{NLTAB.join([construct_plugin_line(plugins[plugin]) for plugin in installed])}
}})
""")
