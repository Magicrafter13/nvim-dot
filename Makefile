default:
# Compile lua config files
	@$(MAKE) -e all --no-print-directory

directories:
	@mkdir -p nvim/lua/plug-set/coc
	@mkdir -p nvim/lua/plug-set/nerdtree

all: directories nvim/lua/plug-set/init.lua nvim/init.lua nvim/lua/clipboard.lua nvim/lua/colorscheme.lua nvim/lua/lazy-init.lua
	@$(MAKE) -s -f nvim/lua/plug-set/settings.make
	@$(MAKE) -s -f nvim/lua/plug-set/lsp.make
# Update/cleanup plugins
	@echo 'Updating plugins...'
	@nvim -u nvim/init.lua -i NONE --headless "+Lazy! update" +qa
# Final cleanup
	@./main/cleanup.bash

clean:
	@rm -rf .plugins nvim/*

config:
	@./init.py

uninstall:
	@./main/uninstall.bash

.PHONY: directories all clean uninstall

nvim/lua/plug-set/settings.make nvim/lua/plug-set/lsp.make: config.json .plugins main/makefiles.py
	@main/makefiles.py $@

nvim/lua/plug-set/nvim-lspconfig.lua: nvim/lua/plug-set/lsp.make
	@$(MAKE) -s -f nvim/lua/plug-set/lsp.make

nvim/lua/plug-set/init.lua: nvim/lua/plug-set/settings.make nvim/lua/plug-set/nvim-lspconfig.lua
	@$(MAKE) -s -f nvim/lua/plug-set/settings.make

# Add init.py as dependency once it is setup to read the config file
config.json:
	@$(MAKE) -e config --no-print-directory

.plugins: config.json configs/base.json configs/env.json configs/yes.json configs/dev.json
	@main/plugins.py

nvim/init.lua: init/0_truecolor.lua init/1_cursor.lua init/2_clipboard.lua init/3_plugins.lua init/80_binary.lua init/81_spell.lua init/90_remaps.lua init/99_general.lua
	@echo -e "\e[1;31mConstructing nvim/init.lua\e[0m"
	@cat init/0_truecolor.lua init/1_cursor.lua init/2_clipboard.lua init/3_plugins.lua init/80_binary.lua init/81_spell.lua init/90_remaps.lua init/99_general.lua > nvim/init.lua

nvim/lua/clipboard.lua: main/clipboard.py config.json configs/base.json
	@main/clipboard.py

nvim/lua/colorscheme.lua: .plugins plugins.json
	@main/colorscheme.py

nvim/lua/lazy-init.lua: .plugins plugins.json
	@main/lazy.py
# Symlink directories and files to standard system locations
	@./main/link.bash
# Install/remove plugins
	@echo 'Installing lazy.nvim + new plugins...'
	@nvim -u nvim/init.lua -i NONE --headless "+Lazy! install" +qa
	@echo 'Cleaning plugins...'
	@nvim -u nvim/init.lua -i NONE --headless "+Lazy! clean" +qa
