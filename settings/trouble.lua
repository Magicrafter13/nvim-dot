require 'trouble'.setup {
	auto_close = true,
	auto_open = false,
}

-- Keymaps

local wk = require("which-key")

wk.add({
	{ "<leader>x", group = "Trouble" },
})

vim.api.nvim_set_keymap('n', '<leader>xx', '<cmd>Trouble diagnostics toggle<cr>', { desc = 'Diagnostics' })
vim.api.nvim_set_keymap('n', '<leader>xs', '<cmd>Trouble symbols toggle<cr>', { desc = 'Symbols' })
vim.api.nvim_set_keymap('n', '<leader>xl', '<cmd>Trouble lsp toggle win.position=right<cr>', { desc = 'LSP Definitions / references / ...' })
