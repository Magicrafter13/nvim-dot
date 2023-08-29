"
" For editing binary files
"
augroup Binary
	au!
	au BufReadPre  *.BIN,*.bin let &bin=1
	au BufReadPost *.BIN,*.bin if &bin | %!xxd
	au BufReadPost *.BIN,*.bin set ft=xxd | endif
	au BufWritePre  *.BIN,*.bin if &bin | %!xxd -r
	au BufWritePre  *.BIN,*.bin endif
	au BufWritePost *.BIN,*.bin if &bin | %!xxd
	au BufWritePost *.BIN,*.bin set nomod | endif
augroup END

