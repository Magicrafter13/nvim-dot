vim.lsp.config.eslint = {
	capabilities = capabilities,
	settings = {
		codeActionOnSave = {
			enable = false,
			mode = "all"
		},
		validate = "on"
	}
}

vim.lsp.config.ts_ls = {
	capabilities = capabilities
}
