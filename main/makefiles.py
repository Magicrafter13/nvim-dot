#!/usr/bin/env python3
"""Construct various Makefiles based on data in .plugins."""

import json
import sys

from utils import read_file, write_file  # pylint: disable=import-error

plugins = json.loads(read_file(".plugins"))["plugins"]
config = json.loads(read_file("config.json"))

LSP = "LSP" in config["programming"]
LSP_REQ = (
    "\techo 'require(\"plug-set/nvim-lspconfig\")' >> nvim/lua/plug-set/"
    "init.lua")
COMP = "Completion" in config["programming"]


def create_settings():
    """Create settings.make."""
    #
    # CREATE nvim/lua/plug-set/settings.make
    # FOR    nvim/lua/plug-set/init.lua
    #
    files = " ".join([f"settings/{plugin}.lua" for plugin in plugins])
    if LSP:
        files += " settings/nvim-lspconfig.lua"
    write_file(
        "nvim/lua/plug-set/settings.make",
        f"""POSSIBLE := {files}
FILES    := $(wildcard settings/*.lua)
EXIST    := $(filter $(POSSIBLE),$(FILES))

nvim/lua/plug-set/init.lua: .plugins $(EXIST)
ifneq ($(EXIST),)
\techo -e '\\e[1;32mCopying plugin settings and adding them to plug-set/init.lua...\\e[0m'
\tcp -u $(EXIST) nvim/lua/plug-set/
\t$(file > nvim/lua/plug-set/init.lua) $(foreach plugin,$(patsubst settings/%.lua,%,$(EXIST)),$(file >> nvim/lua/plug-set/init.lua,require("plug-set/$(plugin)")))
\t{'$(file >> nvim/lua/plug-set/init.lua,require("plug-set/nvim-lspconfig"))' if LSP else ''}
else
\ttouch nvim/lua/plug-set/init.lua
endif
""")  # noqa: E501  pylint: disable=line-too-long


def create_lsp():
    """Create lsp.make."""
    #
    # CREATE nvim/lua/plug-set/lsp.make
    # FOR    nvim/lua/plug-set/nvim-lspconfig.lua
    #
    files = " ".join([
        f"settings/lspconfig/{lang}.lua"
        for lang in config["dev"]])
    if LSP:
        write_file(
            "nvim/lua/plug-set/lsp.make",
            # pylint: disable=C0301
            f"""POSSIBLE := {files}
FILES    := $(wildcard settings/lspconfig/*.lua)
EXIST    := $(filter $(POSSIBLE),$(FILES))

nvim/lua/plug-set/nvim-lspconfig.lua: $(EXIST)
ifneq ($(EXIST),)
\techo -e "\\e[1;32mSetting up LSP config\\e[0m"
\techo "-- Setup language servers." > nvim/lua/plug-set/nvim-lspconfig.lua
\techo "local lspconfig = require('lspconfig')" >> nvim/lua/plug-set/nvim-lspconfig.lua
\techo "vim.diagnostic.config({{virtual_text = false}})" >> nvim/lua/plug-set/nvim-lspconfig.lua
\techo "vim.api.nvim_create_autocmd({{ 'CursorHold', 'CursorHoldI' }}, {{ pattern = '*', callback = function() vim.diagnostic.open_float(nil, {{focus = false}}) end }})" >> nvim/lua/plug-set/nvim-lspconfig.lua
\techo "local capabilities = {"require('cmp_nvim_lsp').default_capabilities()" if COMP else '{}'}" >> nvim/lua/plug-set/nvim-lspconfig.lua
\tcat $(EXIST) >> nvim/lua/plug-set/nvim-lspconfig.lua
else
\ttouch nvim/lua/plug-set/nvim-lspconfig.lua
endif
""")  # noqa: E501
    else:
        write_file("nvim/lua/plug-set/lsp.make", "all:")


if __name__ == "__main__":
    match sys.argv[1]:
        case "nvim/lua/plug-set/settings.make":
            create_settings()
        case "nvim/lua/plug-set/lsp.make":
            create_lsp()
