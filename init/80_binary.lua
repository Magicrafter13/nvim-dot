--
-- For editing binary files
--
local Binary = vim.api.nvim_create_augroup('Binary', { clear = true })
vim.api.nvim_create_autocmd({ 'BufReadPre' }, {
	pattern = { "*.BIN", "*.bin" },
	group = Binary,
	callback = function()
		bin = true
	end
})
vim.api.nvim_create_autocmd({ 'BufReadPost' }, {
	pattern = { "*.BIN", "*.bin" },
	group = Binary,
	callback = function()
		if bin then
			vim.cmd("%!xxd")
			vim.opt.ft = xxd
		end
	end
})
vim.api.nvim_create_autocmd({ 'BufWritePre' }, {
	pattern = { "*.BIN", "*.bin" },
	group = Binary,
	callback = function()
		if bin then
			vim.cmd("%!xxd -r")
		end
	end
})
vim.api.nvim_create_autocmd({ 'BufWritePost' }, {
	pattern = { "*.BIN", "*.bin" },
	group = Binary,
	callback = function()
		if bin then
			vim.cmd("%!xxd")
			vim.opt.mod = false
		end
	end
})
