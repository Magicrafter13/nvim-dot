vim.g.barbar_auto_setup = false
require("barbar").setup {
	animation = true,
	auto_hide = true,
	tabpages = false,
	clickable = true,
	hide = { visible = true },
	highlight_visible = true,
	icons = {
		filetype = {
			custom_colors = false,
			enabled = true
		}
	},
	semantic_letters = true
}
