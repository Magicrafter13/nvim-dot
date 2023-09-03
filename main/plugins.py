#!/usr/bin/python3
"""Construct the lazy-init.lua file (plugin loader)"""

import json
import os
import sys

from utils import read_file, write_file  # pylint: disable=import-error

config = json.loads(read_file(("config.json")))

base = json.loads(read_file(("configs/base.json")))
d = {
    "clipboard": 0,
    "plugins": {}
}
base["default"] = d
env = json.loads(read_file(("configs/env.json")))
yes = json.loads(read_file(("configs/yes.json")))
dev = json.loads(read_file(("configs/dev.json")))

plugins = json.loads(read_file(("plugins.json")))
for pid, val in list(plugins.items()):
    if pid.startswith("_"):
        plugins.pop(pid)
        continue
    if "attributes" not in val:
        val["attributes"] = []
    elif "colorscheme" in val["attributes"] and "colorscheme" not in val:
        val["colorscheme"] = pid
# A set would be better but I want the plugins added in the order we read
# them...
install = []


def set_plugins(plugin_list):
    """Apply changes (like a mask) to an entry in the plugins dictionary"""
    print(f"Called with {plugin_list}")
    for _p in plugin_list:
        if _p in plugins and _p not in install:
            install.append(_p)


def parse_config():
    """Read through user's config file and set plugin data accordingly"""
    # Base
    if len(config["base"]) == 0 or config["base"] not in base:
        config["base"] = "default"
    set_plugins(base[config["base"]]["plugins"])
    # Envs
    for environment in config["environment"]:
        if environment in env:
            set_plugins(env[environment])
    # Yes
    for pack in config["yes"]:
        if pack in yes:
            set_plugins(yes[pack])
    # Dev
    for pack in config["dev"]:
        if pack in dev:
            set_plugins(dev[pack])
    # Colors
    for color in config["colors"]:
        if "colorscheme" in plugins[color]["attributes"]:
            install.append(color)


def copy_lua_script(plug):
    """Copy over the lua script file for a designated plugin (if it exists)"""
    src = f"settings/{plug}.lua"
    if os.path.exists(src):
        os.system(f"cp {src} nvim/lua/plug-set/{plug}.lua")
        with open("nvim/lua/plug-set/init.lua", "a", encoding="UTF-8") as _f:
            _f.write(f'require("plug-set/{plug}")\n')


_NL = "\n"


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


def check_valid_config():
    """Verify the user's config file is properly structured"""
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


def set_colorscheme(name):
    """Set the colorscheme for NeoVim and lightline"""
    data = f'vim.cmd("colorscheme {name}")'
    if "lightline" in install:
        data += f'''local old_lightline = vim.g.lightline or {{}}
old_lightline.colorscheme = "{name}"
vim.g.lightline = old_lightline
vim.call("lightline#enable")'''
    write_file("nvim/lua/colorscheme.lua", f"{data}\n")


if __name__ == "__main__":
    print("\033[1;31mParsing config files\033[0m")
    if not check_valid_config():
        sys.exit(1)
    parse_config()

    print("\033[1;32mSetting up Plugins...\033[0m")
    print(
        "\033[1;31mConstructing nvim/lua/lazy_init.lua... and copying plugin "
        "settings to\n\tnvim/lua/plug-set/\033[0m")
    DATA = """--
-- lazy.nvim
--
vim.g.mapleader = " "

require("lazy").setup({"""
    # Go through plugins dir
    # original_dir = os.getcwd()
    # os.chdir(original_dir + "/plugins")

    # Variable init
    for _plug in install:
        # Read file?
        if _plug in plugins:
            DATA += f"\t{construct_plugin_line(plugins[_plug])}\n"
            copy_lua_script(_plug)
        else:
            print(f"No {_plug} entry found in plugins.json, skipping.")
    DATA += "})\n"

    if "coc" in install:
        # Add global coc variable
        DATA += "vim.g.coc_global_extensions = {"
        DATA += ", ".join([
            f"'{plugins[name]['cocinstall']}'"
            for name in install
            if name in plugins and name.startswith("coc-")])
        DATA += "}\n"
        # Construct settings file
        coc_settings = [
            f"// {name}\n{read_file(f'settings/coc/{name}.json')}"
            for name in install
            if name in plugins and (
                name.startswith("coc-")
                or name == "coc"
            ) and os.path.exists(f"settings/coc/{name}.json")]
        print(f"Contents of settings: {coc_settings}")
        if len(coc_settings) > 0:
            write_file(
                "nvim/coc-settings.json",
                f'{{\n{_NL.join(coc_settings)}\n"": ""\n}}\n')

    write_file("nvim/lua/lazy-init.lua", DATA)
    print("\033[1;31mDone\033[0m")

    # Colorscheme
    print("\033[1;32mSetting colorscheme\033[0m")
    schemes_installed = dict(
        (name, plugins[name])
        for name in install
        if name in plugins and "colorscheme" in plugins[name]["attributes"])
    for k, v in schemes_installed.items():
        if "colorscheme" not in v:
            v["colorscheme"] = k
    if len(schemes_installed) == 0:
        print("No colorschemes were installed! :(")
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
