-- Disable coc-discord-rpc when launched by firenvim
if vim.fn.exists("g:started_by_firenvim") == 1 then
	--vim.fn.CocCommand("rpc.disconnect")
	--vim.fn.CocCommand("rpc.disable")
	vim.cmd("CocCommand rpc.disconnect")
	vim.cmd("CocCommand rpc.disable")
end
