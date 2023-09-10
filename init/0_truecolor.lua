-- Use true color in terminals that support it
if os.getenv("COLORTERM") == "truecolor" then
	vim.opt.termguicolors = true
end
