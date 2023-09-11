require("catppuccin").setup({
	flavor = "macchiato",
	background = {
		dark = "macchiato"
	},
	integrations = {
		barbar = false,
		fidget = false,
		noice = false,
		notify = false,
		treesitter = true,
		ufo = true
	}
})

-- Optional feline config
if require("lazy.core.config").plugins["feline.nvim"] then
	local ctp_feline = require('catppuccin.groups.integrations.feline')
	require("feline").setup({
		components = ctp_feline.get()
	})
end
