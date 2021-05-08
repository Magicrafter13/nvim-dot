#!/bin/bash

# Main directory
echo 'Clearing out ./nvim/'
make clean --no-print-directory

# Check for ${XDG_DATA_DIR}/nvim/plugged, and delete
data="${XDG_DATA_DIR:-$HOME/.local/share}"
if [[ -d "$data" ]]; then
	echo 'Deleting plugins'
	rm -rf "$data"/nvim/plugged
	rm "$data"/nvim/site/autoload/plug.vim
fi

# Remove symlink
config="${XDG_CONFIG_HOME:-$HOME/.config}"
if [[ -L "$config"/nvim ]]; then
	if [[ ! "$config"/nvim/ -ef ./nvim/ ]]; then
		echo "${config}/nvim exists, and is a symbolic link, but does not point to ${PWD}/nvim?"
		echo "Aborting..."
		exit 1
	fi
	echo 'Deleting symbolic link'
	rm "$config"/nvim
fi

# Restore backup
if [[ -d "$config"/nvim.bak ]]; then
	echo 'Backup directory found, restoring'
	mv "$config"/nvim.bak "$config"/nvim
fi
