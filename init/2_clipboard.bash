#!/bin/bash

echo -e '\e[1;32mSetting up Clipboard Provider...\e[0m'
echo -e 'Select System Environment\n\t0) None\n\t1) KDE\n\t2) Xfce' > /dev/stderr

num='temp'
while [[ "$num" == temp ]]; do
	read num
	case "$num" in
		0)
			echo 'Continuing without custom clipboard provider.'
			rm -f nvim/clipboard.vim
			;;
		1)
			echo 'Neovim will use Klipper to Copy/Paste.'
			cp main/kde_clipboard.vim nvim/clipboard.vim
			[ -d "$HOME"/.local/bin/ ] && [ ! -f "$HOME"/.local/bin/klipperCopy ] && cp main/klipperCopy "$HOME"/.local/bin/
			;;
		2)
			echo 'Xfce4 clipboard should work with Neovim out-of-the-box.'
			rm -f nvim/clipboard.vim
			;;
		*) num='temp'
	esac
done
