default:
# Clean some files
	@$(MAKE) -e clean-partial --no-print-directory
# Compile lua config files
	@$(MAKE) -e all --no-print-directory

directories:
	@mkdir -p nvim/lua/plug-set/coc
	@mkdir -p nvim/lua/plug-set/nerdtree

all: directories nvim/init.lua nvim/lua/clipboard.lua nvim/lua/lazy-init.lua
# Symlink directories and files to standard system locations
	@./main/link.bash
# Final cleanup
	@./main/cleanup.bash

clean:
	@rm -rf nvim/*

clean-partial:
	@rm -f nvim/coc-settings.json

uninstall:
	@./main/uninstall.bash

.PHONY: directories all clean clean-partial uninstall

# Add init.py as dependency once it is setup to read the config file
config.json:
	@./init.py

nvim/init.lua: init/0_truecolor.lua init/1_cursor.lua init/2_clipboard.lua init/3_plugins.lua init/80_binary.lua init/81_spell.lua init/90_remaps.lua init/99_general.lua
	@echo -e "\e[1;31mConstructing nvim/init.lua\e[0m"
	@cat init/0_truecolor.lua init/1_cursor.lua init/2_clipboard.lua init/3_plugins.lua init/80_binary.lua init/81_spell.lua init/90_remaps.lua init/99_general.lua > nvim/init.lua

nvim/lua/clipboard.lua: main/clipboard.py config.json configs/base.json
	@main/clipboard.py

nvim/lua/lazy-init.lua: main/plugins.py main/update.bash config.json configs/base.json configs/env.json configs/yes.json configs/dev.json plugins.json
	@rm -rf nvim/lua/plug-set/*.lua nvim/lua/plug-set/coc/*.lua nvim/lua/plug-set/nerdtree/*.lua
	@main/plugins.py
# Update/cleanup plugins
	@./main/update.bash
