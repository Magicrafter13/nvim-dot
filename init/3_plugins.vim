" Make sure vim-plug is installed
let data_dir = stdpath('data') . '/site'
if empty(glob(data_dir . '/autoload/plug.vim'))
	silent execute '!curl -fLo '.data_dir.'/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
	autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif
"" Install any new plugins
"autocmd VimEnter * if len(filter(values(g:plugs), '!isdirectory(v:val.dir)'))
"	\| PlugInstall --sync | source $MYVIMRC
"\| endif

" Initialize Plugins
runtime! vim-plug.vim
" Plugin settings
runtime! plug-set/*.vim

