-- Set cursor on exit
vim.api.nvim_create_autocmd({"VimLeave", "VimSuspend"}, {
	pattern = { "*" },
	command = "set guicursor=a:ver1-blinkon400"
})
