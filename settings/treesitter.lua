vim.api.nvim_create_autocmd({ "BufReadPost", "FileReadPost" }, {
	pattern = "*",
	command = "normal zR"
})

require"nvim-treesitter".setup {
  -- Automatically install missing parsers when entering buffer
  auto_install = true,

	--ignore_install = { "css", "make", "html" },

  highlight = {
    -- `false` will disable the whole extension
    enable = true,

		--disable = { "css", "make", "html" },

    -- Setting this to true will run `:h syntax` and tree-sitter at the same time.
    -- Set this to `true` if you depend on 'syntax' being enabled (like for indentation).
    -- Using this option may slow down your editor, and you may see some duplicate highlights.
    -- Instead of true it can also be a list of languages
    additional_vim_regex_highlighting = false
  },

	incremental_selection = {
		enable = true,
		keymaps = {
			init_selection = '<CR>',
			scope_incremental = '<CR>',
			node_incremental = '<TAB>',
			node_decremental = '<S-TAB>'
		}
	},

	indent = {
		enable = true
	}
}

vim.opt.foldmethod = "expr"
vim.opt.foldexpr = "v:lua.vim.treesitter.foldexpr()"
