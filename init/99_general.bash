#!/bin/bash

echo -e '\e[1;32mSetting colorscheme\e[0m'

declare -A schemes
while read line; do
	num=${line%% *}
	name=${line#* }
	schemes[$num]="$name"
done < nvim/colorschemes.temp
rm -f nvim/colorschemes.temp


case ${#schemes[@]} in
	0)
		echo 'No colorschemes were installed! :('
		exit
		;;
	1)
		echo "colorscheme ${schemes[@]}" >> nvim/init.vim
		[[ -f nvim/plug-set/1_0_lightline.vim ]] && echo "let g:lightline.colorscheme = '${schemes[@]}'" >> nvim/plug-set/1_0_lightline.vim
		;;
	*)
		echo 'More than 1 colorscheme installed, please select one to use by default:'
		for num in "${!schemes[@]}"; do
			echo -e "\t$num) ${schemes[$num]}"
		done
		read selection
		selection=$((selection))
		if [[ -n "${schemes[$selection]}" ]]; then
			echo "colorscheme ${schemes[$selection]}" >> nvim/init.vim
			[[ -f nvim/plug-set/1_0_lightline.vim ]] && echo "let g:lightline.colorscheme = '${schemes[$selection]}'" >> nvim/plug-set/1_0_lightline.vim
		fi
		;;
esac > /dev/stderr

unset schemes
