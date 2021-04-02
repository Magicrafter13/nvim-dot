all: nvim
	@rm -rf nvim/*
	@mkdir -p nvim/plug-set/nerdtree
	# Checking setup
	#if symlink exists ~/.config/nvim (and it links to $PWD/nvim) do nothing
	#otherwise...
	# Constructing nvim/init.vim
	@./main/init.bash

nvim:
	@mkdir nvim
