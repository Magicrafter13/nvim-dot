#!/bin/python3
"""Constructs a full NeoVim configuration directory, using a config file and
other data files."""

import json
import os
import sys


def read_file(filename):
    """Simple file read using with"""
    with open(filename, "r", encoding="UTF-8") as _f:
        return _f.read()


def write_file(filename, data):
    """Simple file write using with"""
    with open(filename, "w", encoding="UTF-8") as _f:
        _f.write(data)


config = json.loads(read_file(("config.json")))

base = json.loads(read_file(("configs/base.json")))
d = {
    "clipboard": 0,
    "plugins": {}
}
base['default'] = d
env = json.loads(read_file(("configs/env.json")))
yes = json.loads(read_file(("configs/yes.json")))
_no = json.loads(read_file(("configs/no.json")))
dev = json.loads(read_file(("configs/dev.json")))

plugins = json.loads(read_file(("plugins.json")))


def set_plugins(changes):
    """Apply changes (like a mask) to an entry in the plugins dictionary"""
    for category, c_obj in changes.items():
        if isinstance(c_obj, bool):
            for plugin in plugins[category]:
                plugins[category][plugin]['default'] = True
        else:
            for plugin, status in c_obj.items():
                plugins[category][plugin]['default'] = status


def parse_config():
    """Read through user's config file and set plugin data accordingly"""
    # Base
    if len(config['base']) == 0 or not config['base'] in base:
        config['base'] = 'default'
    set_plugins(base[config['base']]['plugins'])
    # Envs
    for environment in config['environment']:
        if environment in env:
            set_plugins(env[environment])
    # Yes
    for pack in config['yes']:
        if pack in yes:
            set_plugins(yes[pack])
    # No
    for pack in config['no']:
        if pack in _no:
            set_plugins(_no[pack])
    # Dev
    for pack in config['dev']:
        if pack in dev:
            set_plugins(dev[pack])
    # Colors
    for color in config['colors']:
        if color in plugins['colorschemes']:
            plugins['colorschemes'][color]['default'] = True


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
        with open("nvim/lua/plug-set/init.lua", 'a', encoding="UTF-8") as _f:
            _f.write(f'require("plug-set/{name}")\n')


_NL = '\n'


def construct_plugin_line(category: str, plug: str, plugin: dict):
    """Construct a plugin spec line for use with lazy.nvim"""
    line = f'"{plugin["repo"]}",'
    if "params" in plugin:
        line = f'{{ {line} {plugin["params"]} }},'
    elif category == "nerdtree" and not plug == "nerdtree":
        line = f'{{ {line} dependencies = { "nerdtree" } }},'
    if "comment" in plugin:
        line += f" -- {plugin['comment']}"
    return line


def build_plugins():
    """Construct the lazy_init.lua file (plugin loader)"""
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
        for plug in list(plugins[category]):
            # Read file?
            plugin = plugins[category][plug]
            if plugin['default']:
                line = construct_plugin_line(category, plug, plugin)
                data += f"\t{line}\n"
                copy_lua_script(category, plug)
    if plugins['nerdtree']['nerdtree']['default']:
        data += '\n'
    data += "})\n"
    if plugins['coc']['coc']['default']:
        data += "vim.g.coc_global_extensions = {"
        data += ", ".join([
            f"'{obj['cocinstall']}'"
            for name, obj in plugins['coc'].items()
            if name != 'coc' and obj['default']])
        data += "}\n"
    write_file("nvim/lua/lazy-init.lua", data)
    print('\033[1;31mDone\033[0m')
    # os.chdir(original_dir)
    # Install/Update
    # os.system('main/update.bash')


def set_colorscheme(name):
    """Set the colorscheme for NeoVim and lightline"""
    if plugins['statusbar']['lightline']['default']:
        with open(
            'nvim/lua/plug-set/statusbar_lightline.lua',
            'a',
            encoding="UTF-8"
        ) as _vs:
            _vs.write(f'''local old_lightline = vim.g.lightline or {{}}
old_lightline.colorscheme = "{name}"
vim.g.lightline = old_lightline''')
    return f'vim.cmd("colorscheme {name}")\n'


def create_init():
    """Construct the primary NeoVim config file (init.lua)"""
    # TO-DO: make this more adaptable
    data = "\n".join(read_file(f"init/{_p}") for _p in [
        '0_truecolor.lua',
        '1_cursor.lua',
        '2_clipboard.lua',
        '3_plugins.lua',
        '80_binary.lua',
        '81_spell.lua',
        '90_remaps.lua',
        '99_general.lua'
    ])

    # Read config files
    selected_base = base[
        'default'
        if len(config['base']) == 0 or not config['base'] in base
        else config['base']]

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
    else:
        print("Invalid environment - continuing with setup.")

    # Plugins
    build_plugins()

    # Colorscheme
    print("\033[1;32mSetting colorscheme\033[0m")
    schemes_installed = dict(
        (k, v)
        for k, v in plugins['colorschemes'].items()
        if v['default'])
    if len(schemes_installed) == 0:
        print("No colorschemes were installed! :(")
    elif len(schemes_installed) == 1:
        data += set_colorscheme(
            list(schemes_installed.values())[0]['colorscheme'])
    elif len(config['colors']) > 0:
        data += set_colorscheme(
            schemes_installed[config['colors'][0]]['colorscheme'])
    else:
        print(
            "More than 1 colorscheme installed, please select one to use "
            "by default:")
        for name in schemes_installed:
            print(f"\t{name} - {schemes_installed[name]['comment']}")
        selection = input()
        data += (
            set_colorscheme(schemes_installed[selection]['colorscheme'])
            if selection in schemes_installed else "")

    write_file("nvim/init.lua", data)


def check_valid_config():
    """Verify the user's config file is properly structured"""
    good_config = True
    if not isinstance(config['base'], str):
        print("Error in config file. Expected string for 'base'.")
        good_config = False
    if not isinstance(config['environment'], list):
        print("Error in config file. Expected [] list for 'environment'.")
        good_config = False
    if not isinstance(config['yes'], list):
        print("Error in config file. Expected [] list for 'yes'.")
        good_config = False
    if not isinstance(config['no'], list):
        print("Error in config file. Expected [] list for 'no'.")
        good_config = False
    if not isinstance(config['dev'], list):
        print("Error in config file. Expected [] list for 'dev'.")
        good_config = False
    if not isinstance(config['colors'], list):
        print("Error in config file. Expected [] list for 'colors'.")
        good_config = False
    return good_config


if __name__ == "__main__":
    print("\033[1;31mParsing config files\033[0m")
    if not check_valid_config():
        sys.exit(1)
    parse_config()
    print("\033[1;31mConstructing nvim/init.vim\033[0m")
    create_init()
