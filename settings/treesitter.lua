vim.opt.foldmethod = "expr"
vim.opt.foldexpr = "nvim_treesitter#foldexpr()"

vim.api.nvim_create_autocmd({ "BufReadPost", "FileReadPost" }, {
	pattern = "*",
	command = "normal zR"
})

require"nvim-treesitter.configs".setup {
  -- Automatically install missing parsers when entering buffer
  auto_install = true,

	ignore_install = { "css", "make" },

  highlight = {
		disable = { "css", "make" },

    -- `false` will disable the whole extension
    enable = true,

    -- Setting this to true will run `:h syntax` and tree-sitter at the same time.
    -- Set this to `true` if you depend on 'syntax' being enabled (like for indentation).
    -- Using this option may slow down your editor, and you may see some duplicate highlights.
    -- Instead of true it can also be a list of languages
    additional_vim_regex_highlighting = false
  }
}
