local python_version = vim.trim(vim.fn.system({ "python3", "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" }))
local venv_path = string.format(
	'import sys; sys.path.append("/usr/lib/python%s/site-packages"); import pylint_venv; pylint_venv.inithook(force_venv_activation=True, quiet=True)',
	python_version
)

vim.lsp.config.pylsp = {
	capabilities = capabilities,
	settings = {
		pylsp = {
			plugins = {
				--autopep8 = {
					--enabled = true
				--},
				--flake8 = {
					--enabled = true
				--},
				pylint = {
					enabled = true,
					args = {
						"--init-hook",
						venv_path,
					}
				},
				pydocstyle = {
					enabled = true,
					convention = "pep257"
				}
			}
		}
	}
}
