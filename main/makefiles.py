#!/usr/bin/python3
"""Construct various Makefiles based on data in .plugins"""

import json
import os

from utils import read_file, write_file  # pylint: disable=import-error

plugins = json.loads(read_file(".plugins"))["plugins"]
config = json.loads(read_file("config.json"))

ENL = "\\n"
LSP_REQ = "\techo 'require(\"plug-set/nvim-lspconfig\")' >> nvim/lua/plug-set/init.lua"

if __name__ == "__main__":
    cwd = os.getcwd()

    LSP = "lsp" in config["programming"]

    #
    # CREATE nvim/lua/plug-set/settings.make
    # FOR    nvim/lua/plug-set/init.lua
    #
    FILES = " ".join([f"settings/{plugin}.lua" for plugin in plugins])
    if LSP:
        FILES += " settings/nvim-lspconfig.lua"
    write_file(
        "nvim/lua/plug-set/settings.make",
        f"""POSSIBLE := {FILES}
FILES    := $(wildcard settings/*.lua)
EXIST    := $(filter $(POSSIBLE),$(FILES))

nvim/lua/plug-set/init.lua: .plugins $(EXIST)
ifneq ($(EXIST),)
\techo -e '\\e[1;32mCopying plugin settings and adding them to plug-set/init.lua...\\e[0m'
\tcp -u $(EXIST) nvim/lua/plug-set/
\techo -e '$(foreach file,$(patsubst settings/%.lua,%,$(EXIST)),\\nrequire("plug-set/$(file)"))' > nvim/lua/plug-set/init.lua
{LSP_REQ if LSP else ''}
else
\ttouch nvim/lua/plug-set/init.lua
endif
""")  # pylint: disable=line-too-long

    #
    # CREATE nvim/lua/plug-set/lsp.make
    # FOR    nvim/lua/plug-set/nvim-lspconfig.lua
    #
    FILES = " ".join([
        f"settings/lspconfig/{lang}.lua"
        for lang in config["dev"]])
    if LSP:
        write_file(
            "nvim/lua/plug-set/lsp.make",
            f"""POSSIBLE := {FILES}
FILES    := $(wildcard settings/lspconfig/*.lua)
EXIST    := $(filter $(POSSIBLE),$(FILES))

nvim/lua/plug-set/nvim-lspconfig.lua: $(EXIST)
ifneq ($(EXIST),)
\techo -e "\\e[1;32mSetting up LSP config\\e[0m"
\techo "-- Setup language servers." > nvim/lua/plug-set/nvim-lspconfig.lua
\techo "local lspconfig = require('lspconfig')" >> nvim/lua/plug-set/nvim-lspconfig.lua
\tcat $(EXIST) >> nvim/lua/plug-set/nvim-lspconfig.lua
else
\ttouch nvim/lua/plug-set/nvim-lspconfig.lua
endif
""")
    else:
        write_file("nvim/lua/plug-set/lsp.make", "all:")
