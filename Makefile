all: nvim
	@rm -rf nvim/*
	@mkdir -p nvim/plug-set/nerdtree
	@./main/link.bash
	@./main/init.bash

nvim:
	@mkdir nvim

uninstall:
	@./main/uninstall.bash
