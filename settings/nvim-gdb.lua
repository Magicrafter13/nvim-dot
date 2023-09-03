-- nvim-gdb

--let g:loaded_nvimgdb = 1

-- Single-letter keymaps.
function nvim_gdb_no_tkeymaps()
	vim.keymap.set('t', "<esc>", "<C-\\><C-n>", { silent = true })
end

vim.g.nvimgdb_config_override = {
	key_next = 'n',
	key_step = 's',
	key_finish = 'f',
	key_continue = 'c',
	key_until = 'u',
	key_breakpoint = 'b',
	set_tkeymaps = "v:lua.nvim_gdb_no_tkeymaps"
}

-- Functions
function map_gdb_keys()
	vim.keymap.set('', "<F4>", ":GdbUntil<CR>")
	vim.keymap.set('', "<F8>", ":GdbBreakpointToggle<CR>")
end
vim.api.nvim_create_autocmd({ "Filetype" }, {
	pattern = { "c", "cpp", "h", "hpp" },
	callback = map_gdb_keys
})
