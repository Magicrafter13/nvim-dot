" syntastic
set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*

let g:syntastic_always_populate_loc_list = 1 " remove if conflicts with other plugins arise
let g:syntastic_auto_loc_list = 1
let g:syntastic_check_on_open = 1
let g:syntastic_check_on_wq = 0
let g:syntastic_aggregate_errors = 1
let g:syntastic_id_checkers = 1
let g:syntastic_error_symbol = ""
let g:syntastic_warning_symbol = ""
let g:syntastic_enable_balloons = 0 " Don't have mouse support yet ...

augroup JavaSource
	autocmd BufReadPre *.java if isdirectory("src") |  let g:syntastic_java_javac_classpath = getcwd() . "/src/" | endif
	autocmd BufReadPre *.java if isdirectory("source") |  let g:syntastic_java_javac_classpath = getcwd() . "/source/" | endif
	autocmd BufReadPre *.java if filereadable(".classpath") | let g:syntastic_java_javac_custom_classpath_command = "grep \"kind=\\\"src\\\"\" .classpath | sed -r 's/.*<classpathentry kind=\"src\" path=\"(.*)\"\\/>.*/\\1/'" | endif
augroup END

"augroup JavaClass
"	autocmd BufReadPre *.java if isdirectory("bin") |  let g:syntastic_java_javac_classpath = getcwd() . "/bin/" | endif
"augroup END
