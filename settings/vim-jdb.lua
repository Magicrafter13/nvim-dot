-- ViM jdb
function map_jdb_keys()
	vim.keymap.set('', "<F8>", ":JDBToggleBreakpointOnLine<CR>")
end
vim.api.nvim_create_autocmd({ "Filetype" }, {
	pattern = "java",
	callback = map_jdb_keys
})
