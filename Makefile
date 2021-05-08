cfgs  =
color =

default:
	@[ -f .cfgs ] && cfgs="$$(cat .cfgs)" color=$$([ -f .color ] && cat .color) $(MAKE) -e all --no-print-directory || $(MAKE) -e all --no-print-directory

all: nvim
	@$(MAKE) clean-partial --no-print-directory
	@mkdir -p nvim/plug-set/nerdtree
	@if [ -n "$(cfgs)" ]; then echo > .tmp; [ -n "$(color)" ] && echo $(color) >> .tmp || echo -e "\e[1;31mPress ^D when finished.\e[0m"; fi
	@./main/link.bash
	-@if [ -n "$(cfgs)" ]; then\
			cat $(cfgs:%=configs/%) .tmp $$([ -z "$(color)" ] && echo '-') | ./main/init.bash $$([ -z "$(color)" ] && echo 'nocolor' || echo 'color'); \
			rm .tmp; \
		else \
			./main/init.bash; \
		fi
	@./main/cleanup.bash

nvim:
	@mkdir nvim

clean:
	@rm -rf nvim/*

clean-partial:
	@rm -f nvim/init.vim
	@rm -rf nvim/plug-set/*

uninstall:
	@./main/uninstall.bash

.PHONY: all clean uninstall
