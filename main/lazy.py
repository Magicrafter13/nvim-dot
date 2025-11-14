#!/usr/bin/env python3
"""Construct nvim/lua/lazy-init.lua from .plugins and plugins.json."""

import json

from utils import (  # pylint: disable=import-error
    read_file,
    write_file,
    load_plugins)

installed = json.loads(read_file(".plugins"))["plugins"]
plugins = load_plugins()


def construct_plugin_line(plugin: dict):
    """Construct a plugin spec line for use with lazy.nvim."""
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
vim.keymap.set("n", "<Space>", "<Nop>", {{ remap = false }})
vim.g.mapleader = " "

require("lazy").setup({{
\t{NLTAB.join([
    construct_plugin_line(plugins[plugin])
    for plugin in installed])}
}})
""")
