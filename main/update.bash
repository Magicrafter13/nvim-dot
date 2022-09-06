#!/bin/bash

echo 'Installing vim-plug + new plugins...'
nvim -es -u nvim/init.vim -i NONE +qa <<< ""
echo 'Updating vim-plug...'
nvim -es -u nvim/init.vim -i NONE +PlugUpgrade +qa <<< ""
echo 'Cleaning plugins...'
nvim -es -u nvim/init.vim -i NONE +PlugClean! +qa! <<< "y"
echo 'Updating plugins...'
nvim -es -u nvim/init.vim -i NONE +PlugUpdate +qa <<< ""
