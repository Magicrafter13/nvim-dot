--
-- Neovim editor commands
--
vim.opt.number = true -- Line number
vim.opt.relativenumber = true -- Relative line numbers on lines besides current
vim.opt.tabstop = 2
vim.opt.shiftwidth = 2
vim.opt.wrap = false
vim.opt.fileencoding = "utf8"
vim.opt.encoding = "UTF-8"
vim.opt.updatetime = 100
vim.opt.showmode = false -- Don't show things like -- INSERT --, since lightline is better
vim.opt.hlsearch = true
vim.opt.incsearch = true -- show search results as soon as typing begins, instead of waiting for <CR>
vim.opt.ignorecase = false -- [DEFAULT] don't ignore case when searching
vim.opt.autoindent = false
vim.opt.titlestring = "vim - " .. vim.fn.expand("%:t")
vim.opt.title = true
vim.opt.ruler = false -- [DEFAULT] doesn't show position in file - covered by lightline
vim.opt.confirm = false -- [DEFAULT] don't automatically confirm y/n actions
vim.opt.history = 2000
vim.opt.spell = false -- [DEFAULT] disables spellcheck - who the hell would use this in a code editor???
vim.opt.mouse = "nvc" -- Allow mouse input for normal, visual, and command modes (excluding insert)
-- Set colorscheme (could be important to do before plugins if lazy loaded)
require("colorscheme")
