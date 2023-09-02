#!/usr/bin/python3
"""Construct the lazy-init.lua file (plugin loader)"""

from utils import read_file, write_file

import json
import os

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
install = {}


def set_plugins(changes):
    """Apply changes (like a mask) to an entry in the plugins dictionary"""
    for category, c_obj in changes.items():
        if isinstance(c_obj, bool):
            for plugin in plugins[category]:
                install[category][plugin] = True
        else:
            for plugin in c_obj:
                install[category][plugin] = True


def parse_config():
    """Read through user's config file and set plugin data accordingly"""
    for key, _ in plugins.items():
        install[key] = {}

    # Base
    if len(config["base"]) == 0 or not config["base"] in base:
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
        if color in plugins["colorschemes"]:
            install["colorschemes"][color] = True


def copy_lua_script(category, plug):
    """Copy over the lua script file for a designated plugin (if it exists)"""
    src = f"settings/{category}/{plug}.lua"
    if os.path.exists(src):
        name = ""
        if category in {"coc", "nerdtree"}:
            if category == plug:
                name = category
            else:
                name = f"{category}/{plug}"
        else:
            name = f"{category}_{plug}"
        os.system(f"cp {src} nvim/lua/plug-set/{name}.lua")
        with open("nvim/lua/plug-set/init.lua", "a", encoding="UTF-8") as _f:
            _f.write(f'require("plug-set/{name}")\n')


_NL = "\n"


def construct_plugin_line(category: str, plug: str, plugin: dict):
    """Construct a plugin spec line for use with lazy.nvim"""
    line = f'"{plugin["repo"]}",'
    if "params" in plugin:
        line = f'{{ {line} {", ".join(plugin["params"])} }},'
    elif category == "nerdtree" and not plug == "nerdtree":
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
    if (
        "lightline" in install["statusbar"]
        and install["statusbar"]["lightline"]
    ):
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
    data = """--
-- lazy.nvim
--
vim.g.mapleader = " "

require("lazy").setup({"""
    # Go through plugins dir
    # original_dir = os.getcwd()
    # os.chdir(original_dir + "/plugins")

    # Variable init
    for category in list(plugins):
        data += f"\n\t-- {category}\n"
        for plug in list(install[category]):
            # Read file?
            if install[category][plug]:
                if plug in plugins[category]:
                    line = construct_plugin_line(
                        category,
                        plug,
                        plugins[category][plug])
                    data += f"\t{line}\n"
                    copy_lua_script(category, plug)
                else:
                    print(f"No {plug} entry found in {category}, skipping.")
    data += "})\n"

    if "coc" in install["coc"] and install["coc"]["coc"]:
        # Add global coc variable
        data += "vim.g.coc_global_extensions = {"
        data += ", ".join([
            f"'{plugins['coc'][name]['cocinstall']}'"
            for name, val in install["coc"].items()
            if name != "coc" and val])
        data += "}\n"
        # Construct settings file
        coc_settings = [
            f"// {name}\n{read_file(f'settings/{category}/{name}.json')}"
            for name, obj in install["coc"].items()
            if name in plugins["coc"] and os.path.exists(
                f"settings/{category}/{name}.json")]
        if len(coc_settings) > 0:
            write_file(
                "nvim/coc-settings.json",
                f'{{\n{_NL.join(coc_settings)}\n"": ""\n}}\n')

    write_file("nvim/lua/lazy-init.lua", data)
    print("\033[1;31mDone\033[0m")

    # Colorscheme
    print("\033[1;32mSetting colorscheme\033[0m")
    schemes_installed = dict(
        (k, plugins["colorschemes"][k])
        for k, v in install["colorschemes"].items()
        if v)
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
        for name in schemes_installed:
            print(f"\t{name} - {schemes_installed[name]['comment']}")
        selection = input()
        if selection in schemes_installed:
            set_colorscheme(schemes_installed[selection]["colorscheme"])
