#!/bin/bash

for num in {0..99}; do
	if ls init/${num}_*.vim 1>/dev/null; then
		cat init/${num}_*.vim >> nvim/init.vim
		ls init/${num}_*.bash 1>/dev/null && ./init/${num}_*.bash
	fi
done 2>/dev/null
