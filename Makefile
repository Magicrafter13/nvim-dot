cfgs  =
color =

default:
	@[ -f .config ] && cfgs="$$(sed -nr '/^base=/{s/^base=([^ ]+).*/base_\1/p;q}' .config) $$(sed -nr '/^envs=/{s/^envs=//;s/([^ ]+)/env_\1/g;p;q}' .config) $$(sed -nr '/^yes=/{s/^yes=//;s/([^ ]+)/yes-\1/g;p;q}' .config) $$(sed -nr '/^no=/{s/^no=//;s/([^ ]+)/no-\1/g;p;q}' .config) $$(sed -nr '/^dev=/{s/^dev=//;s/([^ ]+)/dev-\1/g;p;q}' .config)" color=$$(sed -nr '/^color=/{s/^color=([^ ]+).*/\1/p;q}' .config) $(MAKE) -e all --no-print-directory

all: nvim
	@echo $(cfgs)
	@echo $(color)
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

.PHONY: all clean clean-partial uninstall
