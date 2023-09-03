-- syntastic
vim.opt.statusline:append("%#warningmsg#")
vim.opt.statusline:append("%{SyntasticStatuslineFlag()}")
vim.opt.statusline:append("%*")

vim.g.syntastic_always_populate_loc_list = 1 -- remove if conflicts with other plugins arise
vim.g.syntastic_auto_loc_list = 1
vim.g.syntastic_check_on_open = 1
vim.g.syntastic_check_on_wq = 0
vim.g.syntastic_aggregate_errors = 1
vim.g.syntastic_id_checkers = 1
vim.g.syntastic_error_symbol = ""
vim.g.syntastic_warning_symbol = ""
vim.g.syntastic_enable_balloons = 0 -- Don't have mouse support yet ...

local JavaSource = vim.api.nvim_create_augroup("JavaSource", { clear = false })
vim.api.nvim_create_autocmd({ "BufReadPre" }, {
	pattern = "*.java",
	group = JavaSource,
	callback = function()
		if vim.loop.fs_stat("src") then
			vim.g.syntastic_java_javac_classpath = vim.fn.getcwd() .. "/src/"
		end
	end
})
vim.api.nvim_create_autocmd({ "BufReadPre" }, {
	pattern = "*.java",
	group = JavaSource,
	callback = function()
		if vim.loop.fs_stat("source") then
			vim.g.syntastic_java_javac_classpath = vim.fn.getcwd() .. "/source/"
		end
	end
})
vim.api.nvim_create_autocmd({ "BufReadPre" }, {
	pattern = "*.java",
	group = JavaSource,
	callback = function()
		if vim.fn.filereadable(".classpath") then
			vim.g.syntastic_java_javac_custom_classpath_command = "grep \"kind=\\\"src\\\"\" .classpath | sed -r 's/.*<classpathentry kind=\"src\" path=\"(.*)\"\\/>.*/\\1/'"
		end
	end
})

--augroup JavaClass
--	autocmd BufReadPre *.java if isdirectory("bin") |  let g:syntastic_java_javac_classpath = getcwd() . "/bin/" | endif
--augroup END
