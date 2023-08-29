--
-- Spellcheck for applicable files
--
local spellcheck = vim.api.nvim_create_augroup("spellcheck", { clear = true })
vim.api.nvim_create_autocmd({ 'FileType' }, {
	pattern = { "markdown", "latex" },
	group = spellcheck,
	callback = function() vim.cmd("setlocal spell spelllang=en_us") end
})
vim.api.nvim_create_autocmd({ 'BufRead', 'BufNewFile' }, {
	pattern = { "*.md", "*.tex" },
	group = spellcheck,
	callback = function() vim.cmd("setlocal spell spelllang=en_us") end
})
