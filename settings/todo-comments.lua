require("todo-comments").setup {}

vim.keymap.set('n', '<leader>ft', ':TodoTelescope<CR>', { desc = 'Telescope TODO search' })
