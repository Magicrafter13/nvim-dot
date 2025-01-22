--
-- NeoVim Options
--

-- Uncategorized but important
vim.opt.confirm = false -- [DEFAULT] don't automatically confirm y/n actions
vim.opt.history = 2000

-- Line numbers
vim.opt.number = true -- Line number
vim.opt.relativenumber = true -- Relative line numbers on lines besides current

-- Indentation
vim.opt.tabstop = 2
vim.opt.shiftwidth = 2
vim.opt.autoindent = false

-- File display
vim.opt.wrap = false
vim.opt.fileencoding = "utf8"
vim.opt.encoding = "UTF-8"

vim.opt.showmode = false -- Don't show things like -- INSERT --, since lightline is better
vim.opt.ruler = false -- [DEFAULT] doesn't show position in file - covered by lightline

-- Swap file
vim.opt.updatetime = 100

-- Searching
vim.opt.hlsearch = true
vim.opt.incsearch = true -- show search results as soon as typing begins, instead of waiting for <CR>
vim.opt.ignorecase = false -- [DEFAULT] don't ignore case when searching

-- Terminal
vim.opt.titlestring = "vim - " .. vim.fn.expand("%:t")
vim.opt.title = true
vim.opt.spell = false -- [DEFAULT] disables spellcheck - who the hell would use this in a code editor???
vim.opt.mouse = "nvc" -- Allow mouse input for normal, visual, and command modes (excluding insert)

-- Folding
vim.opt.foldenable = true
vim.opt.foldminlines = 3
vim.opt.foldlevel = 99
vim.opt.foldlevelstart = 99

-- Colorscheme (could be important to do before plugins if lazy loaded)
require("colorscheme")
