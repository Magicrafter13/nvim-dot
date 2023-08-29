-- Integrate with system clipboard (Termux API)
vim.g.clipboard = {
	name = "termux",
	copy = {
		["+"] = "termux-clipboard-set",
		["*"] = "termux-clipboard-set"
	},
	paste = {
		["+"] = "termux-clipboard-get",
		["*"] = "termux-clipboard-get"
	}
}
