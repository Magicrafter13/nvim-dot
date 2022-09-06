#!/bin/python3

import json
import os

config = json.loads(open("config.json", "r").read())

base = json.loads(open("configs/base.json", "r").read())
d = dict()
d['clipboard'] = 0
d['plugins'] = dict()
base['default'] = d
env = json.loads(open("configs/env.json", "r").read())
yes = json.loads(open("configs/yes.json", "r").read())
no = json.loads(open("configs/no.json", "r").read())
dev = json.loads(open("configs/dev.json", "r").read())

plugins = json.loads(open('plugins.json', 'r').read())

def set_plugins(changes):
    for category, c_obj in changes.items():
        if type(c_obj) is bool:
            for plugin in plugins[category]:
                plugins[category][plugin]['default'] = True
        else:
            for plugin, status in c_obj.items():
                plugins[category][plugin]['default'] = status

def parse_config():
    # Base
    if not type(config['base']) is str:
        print("Error in config file. Expected string for 'base'.")
    elif len(config['base']) == 0 or not config['base'] in base:
        config['base'] = 'default'
    set_plugins(base[config['base']]['plugins'])
    # Envs
    if not type(config['environment']) is list:
        print("Error in config file. Expected [] list for 'environment'.")
    else:
        for environment in config['environment']:
            if environment in env:
                set_plugins(env[environment])
    # Yes
    if not type(config['yes']) is list:
        print("Error in config file. Expected [] list for 'yes'.")
    else:
        for pack in config['yes']:
            if pack in yes:
                set_plugins(yes[pack])
    # No
    if not type(config['no']) is list:
        print("Error in config file. Expected [] list for 'no'.")
    else:
        for pack in config['no']:
            if pack in no:
                set_plugins(no[pack])
    # Dev
    if not type(config['dev']) is list:
        print("Error in config file. Expected [] list for 'dev'.")
    else:
        for pack in config['dev']:
            if pack in dev:
                set_plugins(dev[pack])
    # Colors
    if not type(config['colors']) is list:
        print("Error in config file. Expected [] list for 'colors'.")
    else:
        for color in config['colors']:
            if color in plugins['colorschemes']:
                plugins['colorschemes'][color]['default'] = True

def copy_vim_script(category, plug):
    src = f"settings/{category}/{plug}.vim"
    if os.path.exists(src):
        dst = 'nvim/plug-set'
        if category == 'coc' or category == 'nerdtree':
            if category == plug:
                dst += f"/{category}.vim"
            else:
                dst += f"/{category}/{plug}.vim"
        else:
            dst += f"/{category}_{plug}.vim"
        os.system(f"cp {src} {dst}")

def build_plugins():
    print("\033[1;32mSetting up Plugins...\033[0m")
    print("\033[1;31mConstructing nvim/vim-plug.vim... and copying plugin settings to nvim/plug-set/\033[0m")
    file = open("nvim/vim-plug.vim", "w", newline = '')
    file.write("\"\n\" Vim-Plug\n\"\ncall plug#begin(stdpath('data') . '/plugged')")
    # Go through plugins dir
    #original_dir = os.getcwd()
    #os.chdir(original_dir + "/plugins")
    # Variable init
    for category in list(plugins):
        file.write(f"\n\" {category}\n")
        # Special category rules
        if category == "coc" or category == "nerdtree":
            if not plugins[category][category]['default']:
                continue
            file.write(f'" {plugins[category][category]["comment"]}\n')
            for sub, obj in plugins[category].items():
                if sub != category and obj['default']:
                    file.write(f'" \t{plugins[category][sub]["comment"]}\n')
                    copy_vim_script(category, sub)
            copy_vim_script(category, category)
            if category == "coc":
                plugin = plugins[category][category]
                line = f'Plug \'{plugin["repo"]}\''
                if "params" in plugin:
                    line += f', {plugin["params"]}'
                file.write(f"{line}\n")
                # Gather settings
                coc_settings = [f"// {name}\n" + open(f"settings/{category}/{name}.json").read() for name, obj in plugins[category].items() if obj['default'] and os.path.exists(f"settings/{category}/{name}.json")]
                if len(coc_settings) > 0:
                    open('nvim/coc-settings.json', 'w').write('{\n' + '\n'.join(coc_settings) + '\n"": ""\n}\n')
                continue
        for plug in list(plugins[category]):
            # Read file?
            plugin = plugins[category][plug]
            if plugin['default']:
                if category == "nerdtree":
                    if plug == "nerdtree":
                        line = f'Plug \'{plugin["repo"]}\''
                        if "params" in plugin:
                            line += f', {plugin["params"]}'
                        file.write(line)
                    else:
                        line = f' |\n\t\\ Plug \'{plugin["repo"]}\''
                        if "params" in plugin:
                            line += f', {plugin["params"]}'
                        file.write(line)
                    continue
                line = f'Plug \'{plugin["repo"]}\''
                if "params" in plugin:
                    line += f', {plugin["params"]}'
                if "comment" in plugin:
                    line += f" \" {plugin['comment']}"
                file.write(f'{line}\n')
                copy_vim_script(category, plug)
    if plugins['coc']['coc']['default']:
        file.write('\ncall plug#end()\nlet g:coc_global_extensions = [')
        file.write(', '.join(["'" + obj['cocinstall'] + "'" for name, obj in plugins['coc'].items() if name != 'coc' and obj['default']]))
        file.write(']\n')
    else:
        file.write('call plug#end()\n')
    print('\033[1;31mDone\033[0m')
    file.close()
    #os.chdir(original_dir)
    # Install/Update
    #os.system('main/update.bash')

def set_colorscheme(rc, name):
    rc.write(f"colorscheme {name}\n")
    if plugins['statusbar']['lightline']['default']:
        with open('nvim/plug-set/statusbar_lightline.vim', 'a') as vs:
            vs.write(f"let g:lightline.colorscheme = '{name}'")
            vs.close()

def create_init():
    rc = open('nvim/init.vim', 'w')
    # TODO: make this more adaptable
    for p in ['0_truecolor.vim', '1_cursor.vim', '2_clipboard.vim', '3_plugins.vim', '80_binary.vim', '81_spell.vim', '90_remaps.vim', '99_general.vim']:
        with open('init/' + p, 'r') as part:
            rc.write(part.read())
            part.close()

    # Read config files
    selected_base = base['default' if len(config['base']) == 0 or not config['base'] in base else config['base']]

    # Clipboard
    print("\033[1;32mSetting up Clipboard Provider...\033[0m")
    # if config doesn't specify, then ask
    if not "clipboard" in selected_base:
        print("Select System Environment\n\t0) None\n\t1) KDE\n\t2) Xfce\n\t3) Termux")
        selected_base['clipboard'] = int(input())
    if selected_base['clipboard'] == 0:
        print("Continuing without custom clipboard provider.")
        os.system('rm -f nvim/clipboard.vim')
    elif selected_base['clipboard'] == 1:
        print("Neovim will use Klipper to Copy/Paste.")
        os.system('cp main/kde_clipboard.vim nvim/clipboard.vim')
        home = os.path.expanduser('~')
        if os.path.exists(home + '/.local/bin') and os.path.isdir(home + '/.local/bin') and not os.path.exists(home + '/.local/bin/klipperCopy'):
            os.system(f'cp main/klipperCopy {home}/.local/bin/')
    elif selected_base['clipboard'] == 2:
        print("Xfce4 clipboard should work with Neovim out-of-the-box.")
        os.system('rm -f nvim/clipboard.vim')
    elif selected_base['clipboard'] == 3:
        print("Neovim will use Termux API. Make sure to install the package, and the corresponding Android package!")
        os.system('cp main/termux_clipboard.vim nvim/clipboard.vim')
    else:
        print("Invalid environment - continuing with setup.")

    # Plugins
    build_plugins()

    # Colorscheme
    print("\033[1;32mSetting colorscheme\033[0m")
    schemes_installed = dict((k, v) for k, v in plugins['colorschemes'].items() if v['default'])
    if len(schemes_installed) == 0:
        print("No colorschemes were installed! :(")
    elif len(schemes_installed) == 1:
        set_colorscheme(rc, schemes_installed.values()[0]['colorscheme'])
    elif len(config['colors']) > 0:
        set_colorscheme(rc, schemes_installed[config['colors'][0]]['colorscheme'])
    else:
        print("More than 1 colorscheme installed, please select one to use by default:")
        for name in schemes_installed:
            print(f"\t{name} - {schemes_installed[name]['comment']}")
        selection = input()
        if selection in schemes_installed:
            set_colorscheme(rc, schemes_installed[selection]['colorscheme'])

print("\033[1;31mParsing config files\033[0m")
parse_config()
print("\033[1;31mConstructing nvim/init.vim\033[0m")
create_init()
