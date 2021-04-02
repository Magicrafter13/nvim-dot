all: nvim
	@rm -rf nvim/*
	@mkdir -p nvim/plug-set/nerdtree
	# Checking setup
	#if symlink exists ~/.config/nvim (and it links to $PWD/nvim) do nothing
	#otherwise...
	@./main/init.bash

nvim:
	@mkdir nvim

uninstall:
	@./main/uninstall.bash
