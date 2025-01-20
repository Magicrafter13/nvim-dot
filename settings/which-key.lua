local wk = require("which-key")

wk.add({
	{ "<leader>f", group = "file" },
	{ "<leader>w", proxy = "<c-w>", group = "windows" },
})
