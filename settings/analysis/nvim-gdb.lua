" nvim-gdb

"let g:loaded_nvimgdb = 1

" Single-letter keymaps.
function! NvimGdbNoTKeymaps()
	tnoremap <silent> <buffer> <esc> <c-\><c-n>
endfunction

let g:nvimgdb_config_override = {
	\ 'key_next': 'n',
	\ 'key_step': 's',
	\ 'key_finish': 'f',
	\ 'key_continue': 'c',
	\ 'key_until': 'u',
	\ 'key_breakpoint': 'b',
	\ 'set_tkeymaps': "NvimGdbNoTKeymaps", 
	\ }

" Functions
autocmd Filetype c,cpp,h,hpp call MapGdbKeys()
function MapGdbKeys()
	noremap <F4> :GdbUntil<CR>
	noremap <F8> :GdbBreakpointToggle<CR>
endfunction
