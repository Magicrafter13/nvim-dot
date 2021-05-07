cfgs =

all: nvim
	@rm -rf nvim/*
	@mkdir -p nvim/plug-set/nerdtree
	@./main/link.bash
	@./main/init.bash
	@./main/cleanup.bash

nvim:
	@mkdir nvim

uninstall:
	@./main/uninstall.bash

config:
	echo -e "\e[1;31mPress ^D when finished.\e[0m"
	@echo -e "\n" > .tmp
	@cat $(cfgs:%=configs/%) .tmp - | $(MAKE) --no-print-directory
	@rm .tmp

.PHONY: all uninstall config
