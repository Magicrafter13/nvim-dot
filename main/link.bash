#!/usr/bin/env bash

config="${XDG_CONFIG_HOME:-$HOME/.config}"

# Checking setup
if [[ -L "$config"/nvim ]]; then
	if [[ ! "$config"/nvim/ -ef ./nvim/ ]]; then
		echo "${config}/nvim exists, and is a symbolic link, but does not point to ${PWD}/nvim?"
		echo "Aborting..."
		exit 1
	fi
else
	if [[ -d "$config"/nvim ]]; then
		echo "Found ${config}/nvim, but it is a directory, not a symbolic link."
		echo 'Would you like to [D]elete this, [B]ack it up, or [I]gnore (for a manual setup)'
		choice=idk
		while [[ "$choice" == idk ]]; do
			read choice
			case "$choice" in
				D) rm -rf "$config"/nvim ;;
				b|B)
					echo "Attempting to back-up..."
					if [[ -d "$config"/nvim.bak ]]; then
						echo "Existing nvim.bak directory found, aborting..."
						exit 1
					fi
					mv "$config"/nvim "$config"/nvim.bak
					;;
				i|I) echo 'If you say so...' ;;
				*) choice=idk ;;
			esac
		done
	fi
	echo -e "\e[1;31mLinking ${config}/nvim --> ${PWD}/nvim\e[0m"
	ln -s "$PWD"/nvim "$config"/nvim
fi
