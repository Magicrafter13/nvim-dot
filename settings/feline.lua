local feline = require("feline")

local components = {
	active = {
		-- left
		{
			{
				provider = {
					name = "vi_mode",
					opts = {
						show_mode_name = true
					}
				},
				hl = function()
					return {
						fg = require("feline.providers.vi_mode").get_mode_color(),
						bg = "darkblue",
						style = "bold",
						name = "NeovimModeHLColor"
					}
				end,
				left_sep = "block",
				right_sep = "block"
			}
		},
		-- middle
		{},
		-- right
		{}
	},
	inactive = {
		-- left
		{},
		-- right
		{}
	}
}

feline.setup({
	components = components
})
