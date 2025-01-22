local builtin = require 'statuscol.builtin'
require 'statuscol'.setup {
	segments = {
		{
			sign = { namespace = { "diagnostic/signs" }, maxwidth = 2, auto = true },
			click = "v:lua.ScSa"
		},
		{ text = { builtin.lnumfunc }, click = "v:lua.ScLa" },
		{ text = { builtin.foldfunc }, click = "v:lua.ScFa" },
		{
			sign = { namespace = { "gitsign" }, maxwidth = 1, auto = true },
			click = "v:lua.ScSa"
		},
		{
			sign = { name = { ".*" }, maxwidth = 2, colwidth = 1, auto = true, wrap = true },
			click = "v:lua.ScSa"
		},
		-- { text = { ' ' } },
	}
}
