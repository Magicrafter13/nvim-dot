all: nvim
	@rm -rf nvim/*
	@mkdir -p nvim/plug-set/nerdtree
	# Constructing nvim/init.vim
	@./main/init.bash

nvim:
	@mkdir nvim
