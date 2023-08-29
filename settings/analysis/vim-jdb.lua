" ViM jdb
autocmd Filetype java call MapJdbKeys()
function MapJdbKeys()
	noremap <F8> :JDBToggleBreakpointOnLine<CR>
endfunction
