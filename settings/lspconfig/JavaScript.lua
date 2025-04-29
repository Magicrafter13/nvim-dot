lspconfig.eslint.setup {
	capabilities = capabilities,
	settings = {
		codeActionOnSave = {
			enable = false,
			mode = "all"
		},
		validate = "on"
	}
}

lspconfig.ts_ls.setup {
	capabilities = capabilities
}
