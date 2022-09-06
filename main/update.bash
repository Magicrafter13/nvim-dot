#!/bin/bash

echo 'Installing vim-plug + new plugins...'
if ! nvim -es -u nvim/init.vim -i NONE +qa <<< ""; then
	nvim -es -u nvim/init.vim -i NONE +PlugInstall +qa <<< ""
fi
echo 'Updating vim-plug...'
nvim -es -u nvim/init.vim -i NONE +PlugUpgrade +qa <<< ""
echo 'Cleaning plugins...'
nvim -es -u nvim/init.vim -i NONE +PlugClean! +qa! <<< "y"
echo 'Updating plugins...'
nvim -es -u nvim/init.vim -i NONE +PlugUpdate +qa <<< ""
