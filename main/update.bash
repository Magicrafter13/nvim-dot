#!/bin/bash

# Original form: nvim -es -u nvim/init.lua -i NONE +qa <<< ""

echo 'Installing lazy.nvim + new plugins...'
#if ! nvim -es -u nvim/init.lua -i NONE +qa <<< ""; then
nvim -u nvim/init.lua -i NONE --headless "+Lazy! install" +qa
#fi
#echo 'Updating vim-plug...'
#nvim -es -u nvim/init.lua -i NONE +PlugUpgrade +qa <<< ""
echo 'Cleaning plugins...'
nvim -u nvim/init.lua -i NONE --headless "+Lazy! clean" +qa
echo 'Updating plugins...'
nvim -u nvim/init.lua -i NONE --headless "+Lazy! update" +qa
