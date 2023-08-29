default:
	@$(MAKE) -e all --no-print-directory

all: config.json nvim
# Clean some files
	@$(MAKE) clean-partial --no-print-directory
	@mkdir -p nvim/lua/plug-set/coc nvim/lua/plug-set/nerdtree
# Symlink directories and files to standard system locations
	@./main/link.bash
# Compile vim-script config files
	@./build.py
# Update/cleanup plugins
	@./main/update.bash
# Final cleanup
	@./main/cleanup.bash

clean:
	@rm -rf nvim/*

clean-partial:
	@rm -f nvim/init.lua
	@rm -f nvim/coc-settings.json
	@rm -rf nvim/lua/plug-set/*

uninstall:
	@./main/uninstall.bash

.PHONY: all clean clean-partial uninstall

nvim:
	@mkdir nvim

config.json:
	@./init.py
