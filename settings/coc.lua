-- Accept completion suggestion with enter.
--inoremap <expr> <cr> pumvisible() ? "\<C-y>" : "\<C-g>u\<CR>"
--inoremap <silent><expr> <cr> pumvisible() ? coc#_select_confirm() : "\<C-g>u\<CR>"

--inoremap <silent><expr> <cr> pumvisible() ? coc#_select_confirm() : "\<C-g>u\<CR>\<c-r>=coc#on_enter()\<CR>"

-- Navigate completion list with Tab and shift Tab.
--inoremap <expr> <Tab> pumvisible() ? "\<C-n>" : "\<Tab>"
--inoremap <expr> <S-Tab> pumvisible() ? "\<C-p>" : "\<S-Tab>"

-- Use <c-space> to trigger completion
vim.keymap.set('i', '<c-space>', function() vim.fn["coc#refresh"]() end, { silent = true, expr = true })

-- Highlight the symbol and its references when holding the cursor.
vim.api.nvim_create_autocmd({ "CursorHold" }, {
	pattern = "*",
	callback = function()
		vim.fn.CocActionAsync('highlight')
	end
})

-- Symbol renaming.
vim.keymap.set('n', '<leader>rn', '<Plug>(coc-rename)', { remap = true })

-- Use autocmd to force lightline update
vim.api.nvim_create_autocmd({ "User" }, {
	pattern = { "CocStatusChange", "CocDiagnosticChange" },
	callback = function()
		vim.fn["lightline#update"]()
	end
})
