local cmp = require('cmp')

cmp.setup({
	snippet = {
		expand = function(args)
			vim.snippet.expand(args.body) -- native NeoVim snippets
		end,
	},
	window = {
		completion = cmp.config.window.bordered(),
		documentaton = cmp.config.window.bordered(),
	},
	mapping = cmp.mapping.preset.insert({
		['<C-b>'] = cmp.mapping.scroll_docs(-4),
		['<C-f>'] = cmp.mapping.scroll_docs(4),
		['<C-Space>'] = cmp.mapping.complete(),
		['<C-e>'] = cmp.mapping.abort(),
		['<CR>'] = cmp.mapping.confirm({ select = true }),
	}),
	sources = cmp.config.sources({
		{ name = 'nvim_lsp' },
	}, {
		{ name = 'buffer' },
	})
})

--local capabilities = require('cmp_nvim_lsp').default_capabilities()
