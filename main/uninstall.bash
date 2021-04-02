#!/bin/bash -x

# Main directory
echo 'Clearing out ./nvim/'
rm -r nvim/*

# Check for ${XDG_DATA_DIR}/nvim/plugged, and delete
if [[ -d ${XDG_DATA_DIR:-~/.local/share}/nvim ]]; then
	echo 'Deleting plugins'
	rm -rf ${XDG_DATA_DIR:-~/.local/share}/nvim/plugged
	rm ${XDG_DATA_DIR:-~/.local/share}/nvim/site/autoload/plug.vim
fi
