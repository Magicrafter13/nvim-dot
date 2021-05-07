cfgs =
color =

default:
	@[ -f .cfgs ] && cfgs="$$(cat .cfgs)" color=$$([ -f .color ] && cat .color) $(MAKE) -e config --no-print-directory || $(MAKE) -e all --no-print-directory

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
	@echo -e "\e[1;31mPress ^D when finished.\e[0m"
	@echo > .tmp
	@[ -n "$(color)" ] && echo $(color) >> .tmp
	@cat $(cfgs:%=configs/%) .tmp $$([ -z "$(color)" ] && echo '-') | $(MAKE) all --no-print-directory
	@rm .tmp

.PHONY: all uninstall config
