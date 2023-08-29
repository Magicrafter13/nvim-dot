"
" Spellcheck for applicable files
"
augroup spellcheck
	autocmd!
	autocmd FileType markdown,latex setlocal spell spelllang=en_us
	autocmd BufRead,BufNewFile *.md,*.tex setlocal spell spelllang=en_us
augroup END

