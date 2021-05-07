#!/bin/bash

# Top
echo -e '\e[1;31mConstructing nvim/init.vim\e[0m'

for num in {0..99}; do
	if ls init/${num}_*.vim 1>/dev/null 2>/dev/null; then
		cat init/${num}_*.vim >> nvim/init.vim
		if ls init/${num}_*.bash 1>/dev/null 2>/dev/null; then
			./init/${num}_*.bash 2>$([ -n "$1" ] && [[ $num -lt 99 || "$1" == color ]] && echo '/dev/null' || echo '/dev/stderr')
			echo
		fi
	fi
done
