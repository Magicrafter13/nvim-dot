#!/bin/bash

echo -e 'Setting up Clipboard Provider...\n'
echo -e 'Select System Environment\n\t0) None\n\t1) KDE\n\t2) Xfce'

num='temp'
while [[ "$num" == temp ]]; do
	read num
	case "$num" in
		0) echo 'Continuing without custom clipboard provider.' ;;
		1)
			echo 'Neovim will use Klipper to Copy/Paste.'
			cp main/kde_clipboard.vim nvim/clipboard.vim
			#cp main/klipperCopy ~/.local/bin/
			;;
		2) echo 'Xfce4 clipboard should work with Neovim out-of-the-box.' ;;
		*) num='temp'
	esac
done
