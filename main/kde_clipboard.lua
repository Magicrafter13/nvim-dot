-- Integrate with system clipboard (KDE's Klipper)
vim.g.clipboard = {
	name = "klipper",
	copy = {
		["+"] = "klipperCopy",
		["*"] = "xclip -i -selection clipboard"
	},
	paste = {
		["+"] = "qdbus org.kde.klipper /klipper getClipboardContents",
		["*"] = "xclip -o -selection clipboard"
	},
	cache_enabled = true
}
