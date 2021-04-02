" lightline
set laststatus=2
let g:lightline = {
	\   'active': {
	\     'left':  [ [ 'mode', 'paste', 'filename' ],
	\                [ 'modread', 'git' ],
	\                [ 'message' ] ],
	\     'right': [ [ 'lineinfo' ],
	\                [ 'percent' ],
	\                [ 'charhex', 'formtype', 'encoding' ] ],
	\   },
	\   'inactive': {
	\     'left':  [ [ 'filename' ],
	\                [ 'git', 'modread' ],
	\                [ ] ],
	\     'right': [ [ 'lineinfo' ],
	\                [ 'percent' ],
	\                [ 'charhex', 'formtype', 'encoding' ] ],
	\   },
	\   'component': {
	\     'charhex':  '0x%B',
	\   },
	\   'component_function': {
	\     'git':      'GitBranch',
	\     'message':  'NameTime',
	\     'modread':  'ModifiedReadonly',
	\     'encoding': 'Encoding',
	\     'formtype': 'FormatAndType',
	\     'mode':     'Mode',
	\     'filename': 'FileName',
	\     'lineinfo': 'Lineinfo',
	\   },
	\   'separator':    { 'left': '', 'right': '' },
	\   'subseparator': { 'left': '', 'right': '' },
	\ }

function! GitBranch()
	try
		if expand('%:t') !~? 'Tagbar\|NERD' && &filetype !=# 'help' && exists ('*FugitiveHead)')
			let mark = ''
			let branch = FugitiveHead()
			return branch !=# '' ? mark.branch : ''
		endif
	catch
	endtry
	return ''
endfunction

function! NameTime()
	return winwidth(0) > 88 ? (' Matthew Rease' . (winwidth(0) > 107 ? (' ' . strftime("%b %d %H:%M")) : '') . ' ') : ''
endfunction

function! ModifiedReadonly()
	let modside = &filetype !=# 'help' ? (&modifiable && &modified ? '!' : '') : ''
	let rdlside = &readonly ? (&filetype !=# 'help' ? '' : '') : ''
	return modside . (modside !=# '' ? (rdlside !=# '' ? ' | ' : '') : '') . rdlside
endfunction

function! FormatAndType()
	let fname = expand('%:t')
	return fname =~# '^__Tagbar__\|NERD_tree' ? '' :
		\ &filetype ==# 'help' ? 'help' :
		\ winwidth(0) > 70 ? &fileformat . ' ' . WebDevIconsGetFileFormatSymbol() . '  ' . (strlen(&filetype) ? &filetype . ' ' . WebDevIconsGetFileTypeSymbol() : 'no ft') : ''
endfunction

function! Encoding()
	let fname = expand('%:t')
	return fname =~# '^__Tagbar__\|NERD_tree' || &filetype ==# 'help' ? '' : &encoding
endfunction

function! Mode()
	let fname = expand('%:t')
	return fname =~# '^__Tagbar__' ? 'Tagbar' :
		\ fname =~# 'NERD_tree' ? 'NERDTree' :
		\ &filetype ==# 'help' ? '' :
		\ winwidth(0) > 60 ? lightline#mode() : ''
endfunction

function! FileName()
	let fname = expand('%:t')
	return fname =~# '^__Tagbar__\|NERD_tree' ? '' :
		\ fname !=# '' ? fname : '[No Name]'
endfunction

function! Lineinfo()
	let fname = expand('%:t')
	return fname =~# '^__Tagbar__\|NERD_tree' ? '' : ' ' . printf('%3d', line('.')) . ':' . col('.')
endfunction
