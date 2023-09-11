local symbols = {
	modified = '  !',
	readonly = is_not_help and ' ' or ' 󰑴'
}

function is_not_help()
	return not (vim.o.filetype == "help")
end

require("lualine").setup {
	options = {
		component_separators = '|',
		section_separators = { left = '', right = '' },
		disabled_filetypes = { 'nerdtree', 'tagbar' },
		always_divide_middle = true,
		--globalstatus = true
	},
	sections = {
		lualine_a = {
			{ 'mode', separator = { left = '' }, padding = { right = 2 }, cond = is_not_help },
			{ 'filename', symbols = symbols }
		},
		lualine_b = {
			{ 'branch', icon = '' },
			'diff' },
		lualine_c = { 'diagnostics', function() return ' Matthew Rease ' .. vim.fn.strftime('%b %d %H:%M') .. ' ' end },
		lualine_x = { 'searchcount', 'selectioncount' },
		lualine_y = { 'fileformat', 'filetype' },
		lualine_z = {
			{ '%B', fmt = function(str) return '0x' .. str end },
			{ 'location', icon = '' },
			{ 'progress', separator = { right = '' }, padding = { left = 2 } }
		}
	},
	inactive_sections = {
		lualine_a = {
			{ 'filename', separator = { left = '', right = '' }, padding = { right = 2 }, symbols = symbols },
			'diff',
			'diagnostics'
		},
		lualine_b = {},
		lualine_c = {},
		lualine_x = {},
		lualine_y = {},
		lualine_z = {
			{ 'progress', separator = { left = '', right = '' }, padding = { left = 2 } }
		}
	}
}
