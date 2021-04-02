#!/bin/bash

declare -A pluginChanges

schemes=()

nerdtree_step=0
end_block=
nerdtree_addon=' |\n\t\\ '

echo -e '\e[1;32mSetting up Plugins...\e[0m'

# Ask about customization
echo 'Would you like to change which plugins to install [n]ow or during [l]oop, or use [d]efaults?'
whatToDo=
while [[ "$whatToDo" != n && "$whatToDo" != l && "$whatToDo" != d ]]; do
	read whatToDo
done
echo

# Determine plugins if [n]ow selected
if [[ $whatToDo == n ]]; then
	echo "Please change plugin defaults using number pairs, like so: category plugin yes/no"
	echo -e "Example:\n\t1 0 no\nto disable lightline."
	echo "Press enter (on a blank line) when finished."
	read request
	while [[ "$request" != "" ]]; do
		if [[ -z "$(sed -r 's/^[0-9]+ [0-9]+ (yes|no)( .*)?$//' <<< "$request")" ]]; then
			array=()
			for delim in $(xargs <<< $request); do
				[[ ${#array[@]} -eq 3 ]] && continue
				array+=($delim)
			done
			pluginChanges["${array[0]}, ${array[1]}"]=${array[2]}
		else
			echo "Invalid Input:\n\t$request"
		fi
		read request
	done
fi

# nvim/vim-plug.vim
echo 'Constructing nvim/vim-plug.vim + copying plugin settings to nvim/plug-set/'
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

			case $whatToDo in
				n)
					plugNum="${plug%%_*}"
					if [[ -n "${pluginChanges["${cat}, ${plugNum}"]}" ]]; then
						data[default]=$pluginChanges["${cat}, ${plugNum}"]
					fi
					;;
				l)
					echo -e "Plugin \e[1;33m'${data[repo]}'\e[0m with comment \e[1;33m${data[comment]}\e[0m"
					echo 'Install this plugin? [Y/N]'
					yesNo=
					while [[ -z "$yesNo" ]]; do
						read yesNo
						case "$yesNo" in
							y|Y) yesNo=yes ;;
							n|N) yesNo=no ;;
							*) yesNo= ;;
						esac
					done
					data[default]=$yesNo
					;;
				d) ;;
			esac

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

				# If plugin is a colorscheme (or adds one), add it to the array
				[[ -n "${data[colorscheme]}" ]] && schemes+=("${data[colorscheme]}")
			fi

			unset data

			[[ $nerdtree_step -eq 1 && "${plug#*_}" == nerdtree ]] && nerdtree_step=2
		done
	fi
	echo -e "$end_block" >> ../nvim/vim-plug.vim
done
cd ..
echo 'call plug#end()' >> nvim/vim-plug.vim

unset pluginChanges

# Create colorscheme file
for scheme in ${schemes[@]}; do
	echo "$scheme" >> nvim/colorschemes.temp
done

# Install/Update
echo 'Installing vim-plug + new plugins...'
nvim -es -u nvim/init.vim -i NONE +qa
echo 'Updating vim-plug...'
nvim -es -u nvim/init.vim -i NONE +PlugUpgrade +qa
echo 'Cleaning plugins...'
nvim -u nvim/init.vim -i NONE +PlugClean +qa! <<< "y"
echo 'Updating plugins...'
nvim -es -u nvim/init.vim -i NONE +PlugUpdate +qa
