require 'mason-lspconfig'.setup {
	automatic_installation = false -- TODO: set to true once noice fixes themselves (msg_scroll_flush: Assertion `to_scroll >= 0' failed)
}

require 'mason-lspconfig'.setup_handlers {
	function (server_name)
		require("lspconfig")[server_name].setup {}
	end
}
