#!/bin/bash -x

echo -e '\e[1;32mSetting colorscheme\e[0m'

schemes=()
while read line; do
	schemes+=("$line")
done < nvim/colorschemes.temp
rm nvim/colorschemes.temp

case ${#schemes} in
	0)
		echo 'No colorschemes were installed! :('
		exit
		;;
	1)
		echo "colorscheme ${schemes[0]}" >> nvim/init.vim
		[[ -f nvim/plug-set/1_0_lightline.vim ]] && echo "let g:lightline.colorscheme = '${schemes[0]}'" >> nvim/plug-set/1_0_lightline.vim
		;;
	*)
		echo 'More than 1 colorscheme installed, please select one to use by default:'
		i=0
		for scheme in "${schemes[@]}"; do
			echo -e "\t$((i + 1))) $scheme"
			i=$((i + 1))
		done
		selection=0
		while [[ $selection -lt 1 || $selection -gt $i ]]; do
			read selection
			selection=$((selection))
		done
		echo "colorscheme ${schemes[$((selection - 1))]}" >> nvim/init.vim
		[[ -f nvim/plug-set/1_0_lightline.vim ]] && echo "let g:lightline.colorscheme = '${schemes[$((selection - 1))]}'" >> nvim/plug-set/1_0_lightline.vim
		;;
esac
