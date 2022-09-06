cfgs  =
colors =

default:
	@[ -f .config ] && cfgs="$$(sed -nr '/^base=/{s/^base=([^ ]+).*/base_\1/p;q}' .config) $$(sed -nr '/^envs=/{s/^envs=//;s/([^ ]+)/env_\1/g;p;q}' .config) $$(sed -nr '/^yes=/{s/^yes=//;s/([^ ]+)/yes-\1/g;p;q}' .config) $$(sed -nr '/^no=/{s/^no=//;s/([^ ]+)/no-\1/g;p;q}' .config) $$(sed -nr '/^dev=/{s/^dev=//;s/([^ ]+)/dev-\1/g;p;q}' .config)" colors=$$(sed -nr '/^colors=/{s/^colors=\s*([0-9 ]+).*/\1/p;q}' .config) $(MAKE) -e all --no-print-directory

all: nvim
# Clean some files
	@$(MAKE) clean-partial --no-print-directory
	@mkdir -p nvim/plug-set/coc nvim/plug-set/nerdtree
# Get list of colors
#	@if [ -n "$(cfgs)" ]; then echo > .tmp; [ -n "$(colors)" ] && echo $(word 1,$(colors)) >> .tmp || echo -e "\e[1;31mPress ^D when finished.\e[0m"; fi
# Symlink directories and files to standard system locations
	@./main/link.bash
# Construct input lines for each colorscheme the user wants installed
#	-@if [ -n "$(colors)" ]; then\
#			for color in $(colors); do\
#				echo "0 $$color yes" >> .colors;\
#			done;\
#		fi
# Pass all config input lines to main/init.bash
#	-@if [ -n "$(cfgs)" ]; then\
#			cat $(cfgs:%=configs/%)$$([ -n "$(colors)" ] && echo ' .colors') .tmp$$([ -z "$(colors)" ] && echo ' -') | ./main/init.bash $$([ -z "$(colors)" ] && echo 'nocolor' || echo 'color'); \
#			rm .tmp; \
#			rm -f .colors; \
#		else \
#			./main/init.bash; \
#		fi
	@./build.py
	@./main/update.bash
	@./main/cleanup.bash

nvim:
	@mkdir nvim

clean:
	@rm -rf nvim/*

clean-partial:
	@rm -f nvim/init.vim
	@rm -f nvim/coc-settings.json
	@rm -rf nvim/plug-set/*

uninstall:
	@./main/uninstall.bash

.PHONY: all clean clean-partial uninstall
