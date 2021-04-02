#!/bin/bash

schemes=()

nerdtree_step=0
end_block=
nerdtree_addon=' |\n\t\\ '

# Ask about customization
echo 'Would you like to change which plugins to install [n]ow or during [l]oop, or use [d]efaults?'
whatToDo=
while [[ "$whatToDo" != n && "$whatToDo" != l && "$whatToDo" != d ]]; do
	read whatToDo
done

# nvim/vim-plug.vim
echo 'Constructing nvim/vim-plug.vim, and copying custom plugin settings to nvim/plug-set/'
echo -e "\"\n\" Vim-Plug\n\"\ncall plug#begin(stdpath('data') . '/plugged')" > nvim/vim-plug.vim
cd plugins
for cat in {0..9}; do
	category=`ls -d ${cat}_* 2>/dev/null`
	if [[ -n "${category}" ]]; then
		[[ "${category#*_}" == nerdtree ]] && nerdtree_step=1
		echo "\" $category" >> ../nvim/vim-plug.vim
		for plug in ${category}/*; do
			plug="${plug#${category}/}"
			[[ "$plug" == settings ]] && continue

			declare -A data

			# Read file
			while read line; do
				[[ -z "$line" ]] && continue

				key="${line%%=*}"
				val="${line#*=}"
				data[$key]="$val"
			done < ${category}/${plug}

			# Place plugin in file (if requested) TODO: add ability to manually include/exclude plugins instead of using default
			if [[ ${data[default]} == yes ]]; then
				plug_line="Plug '${data[repo]}'"
				[[ -n "${data[params]}" ]] && plug_line="${plug_line}, ${data[params]}"
				if [[ $nerdtree_step -eq 0 ]]; then
					echo "$plug_line \" ${data[comment]}" >> ../nvim/vim-plug.vim
				else
					echo -e "\" $([[ $nerdtree_step -eq 2 ]] && echo '\t')${data[comment]}" >> ../nvim/vim-plug.vim
					[[ $nerdtree_step -eq 2 ]] && end_block="${end_block}${nerdtree_addon}${plug_line}" || end_block="$plug_line"
					#end_block="$end_block"$([[ $nerdtree_step -eq 2 ]] && echo "'"' |\\n\\t\\\\ '"'")"${plug_line}"
				fi
				[[ -f ${category}/settings/${plug}.vim ]] && cp ${category}/settings/${plug}.vim ../nvim/plug-set/$([[ $nerdtree_step -lt 2 ]] && echo "${cat}_" || echo 'nerdtree/')${plug}.vim
			fi

			# If plugin is a colorscheme (or adds one), add it to the array
			[[ -n "${data[colorscheme]}" ]] && schemes+=("${data[colorscheme]}")

			unset data

			[[ $nerdtree_step -eq 1 && "${plug#*_}" == nerdtree ]] && nerdtree_step=2
		done
	fi
	echo -e "$end_block" >> ../nvim/vim-plug.vim
done
cd ..
echo 'call plug#end()' >> nvim/vim-plug.vim

# Create colorscheme file
for scheme in ${schemes[@]}; do
	echo "$scheme" >> nvim/colorschemes.temp
done

# Install/Update
echo 'Installing vim-plug, and installing any plugins that aren'\''t already installed...'
nvim -es -u nvim/init.vim -i NONE +qa
echo 'Upgrading vim-plug if possible...'
nvim -es -u nvim/init.vim -i NONE +PlugUpgrade +qa
echo 'Cleaning plugins...'
nvim -es -u nvim/init.vim -i NONE +PlugClean +qa
echo 'Updating plugins if possible...'
nvim -es -u nvim/init.vim -i NONE +PlugInstall +qa
#echo 'Upgrading vim-plug, cleaning plugins, updating plugins, and installing any new plugins...'
#nvim -es -u nvim/init.vim -i NONE +PlugUpgrade +PlugClean +PlugUpdate +PlugInstall +qa
