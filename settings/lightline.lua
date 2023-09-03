-- lightline
vim.opt.laststatus = 2
vim.g.lightline = {
	active = {
		left = { { "mode", "paste", "filename" },
		         { "modread", "git", "cocstatus" },
		         { "message" } },
		right = { { "lineinfo" },
		          { "percent" },
		          { "charhex", "formtype", "encoding" } },
	},
	inactive = {
		left = { { "filename" },
		         { "git", "modread" },
		         { } },
		right = { { "lineinfo" },
		          { "percent" },
		          { "charhex", "formtype", "encoding" } },
	},
	component = {
		charhex = "0x%B"
	},
	component_function = {
		git       = "GitBranch",
		message   = "NameTime",
		modread   = "ModifiedReadOnly",
		encoding  = "Encoding",
		formtype  = "FormatAndType",
		mode      = "Mode",
		filename  = "FileName",
		lineinfo  = "Lineinfo",
		cocstatus = "CocStatus"
	},
	separator    = { left = "", right = "" },
	subseparator = { left = "", right = "" }
}

function NameTime()
	local w = vim.fn.winwidth(0)
	if w < 89 then return "" end
	local name = " Matthew Rease"
	if vim.fn.winwidth(0) > 107 then
		name = name .. ' ' .. vim.fn.strftime("%b %d %H:%M")
	end
	return name
end

-- It's just not worth making these all lua, honestly

--function ModifiedReadonly()
--	local modside = ""
--	local help = vim.o.filetype == "help"
--	if not help and vim.o.modifiable and vim.o.modified then
--		modside = "!"
--	end
--	local rdlside = ""
--	if vim.o.readonly then
--		if help then
--			rdlside = ""
--		else
--			rdlside = ""
--		end
--	end
--	if not modside == "" and not rdlside == "" then
--		return modside .. ' | ' .. rdlside
--	end
--	return modside .. rdlside
--end

vim.api.nvim_exec([[
function! GitBranch()
	try
		if expand('%:t') !~? 'Tagbar\|NERD' && &filetype !=# 'help' && exists ('*FugitiveHead')
			let mark = ''
			let branch = FugitiveHead()
			return branch !=# '' ? mark.branch : ''
		endif
	catch
	endtry
	return ''
endfunction

function! NameTime()
	return v:lua.NameTime()
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
		\ winwidth(0) > 70 ? &fileformat . (exists ('*WebDevIconsGetFileFormatSymbol') ? ' ' . WebDevIconsGetFileFormatSymbol() : '') . '  ' . (strlen(&filetype) ? &filetype . (exists ('*WebDevIconsGetFileTypeSymbol') ? ' ' . WebDevIconsGetFileTypeSymbol() : '') : 'no ft') : ''
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

function! CocStatus()
	return exists("*coc#status") ? coc#status() : ''
endfunction
]], true)
