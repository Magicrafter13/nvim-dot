#!/bin/bash

declare -A pluginChanges

schemes=()

coc_enabled=no
coc_step=0
coc_block=
coc_extra=
nerdtree_step=0
nerdtree_block=
addon=' |\n\t\\ '

echo -e '\e[1;32mSetting up Plugins...\e[0m'

# Ask about customization
{
echo 'Would you like to change which plugins to install [n]ow or during [l]oop, or use [d]efaults?'
whatToDo=
while [[ "$whatToDo" != n && "$whatToDo" != l && "$whatToDo" != d ]]; do
	read whatToDo
done
echo
} > /dev/stderr

# Determine plugins if [n]ow selected
{
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
} > /dev/stderr

# nvim/vim-plug.vim
echo -e '\e[1;31mConstructing nvim/vim-plug.vim...\e[0m and copying plugin settings to nvim/plug-set/'
echo -e "\"\n\" Vim-Plug\n\"\ncall plug#begin(stdpath('data') . '/plugged')" > nvim/vim-plug.vim
cd plugins
for cat in {0..9}; do
	category=`ls -d ${cat}_* 2>/dev/null`
	if [[ -n "${category}" ]]; then
		[[ "${category#*_}" == coc ]] && coc_step=1
		[[ "${category#*_}" == nerdtree ]] && coc_step=0 nerdtree_step=1 && echo >> ../nvim/vim-plug.vim
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
						data[default]=${pluginChanges["${cat}, ${plugNum}"]}
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
				if [[ $coc_step -eq 0 && $nerdtree_step -eq 0 ]]; then
					[[ $plugNum -eq 0 && $cat -eq 8 ]] && coc_enabled=yes
					echo "$plug_line \" ${data[comment]}" >> ../nvim/vim-plug.vim
				elif [[ $cat -eq 8 && $coc_enabled == yes ]] || [[ $cat -ne 8 ]]; then
					echo -e "\" $([[ $coc_step -eq 2 || $nerdtree_step -eq 2 ]] && echo '\t')${data[comment]}" >> ../nvim/vim-plug.vim
					case $coc_step in
						2)
							coc_block="${coc_block}${addon}${plug_line}"
							coc_extra="$([[ -z "$coc_extra" ]]  && echo 'let g:coc_global_extensions = [' || echo "${coc_extra}, ")'${data[cocinstall]}'"
							;;
						1) coc_block="$plug_line" ;;
					esac
					case $nerdtree_step in
						2) nerdtree_block="${nerdtree_block}${addon}${plug_line}" ;;
						1) nerdtree_block="$plug_line" ;;
					esac
				fi
				[[ -f ${category}/settings/${plug}.vim ]] && cp ${category}/settings/${plug}.vim ../nvim/plug-set/$([[ $coc_step -lt 2 && $nerdtree_step -lt 2 ]] && echo "${cat}_" || echo $([ $coc_step -eq 2 ] && echo 'coc' || echo 'nerdtree')'/')${plug}.vim
				[[ $coc_step -gt 0 ]] && [[ -f ${category}/settings/${plug}.json ]] && cat ${category}/settings/${plug}.json >> ../nvim/coc-settings.json

				# If plugin is a colorscheme (or adds one), add it to the array
				[[ -n "${data[colorscheme]}" ]] && schemes+=("${data[colorscheme]}")
			fi

			unset data

			[[ $coc_step -eq 1 && "${plug#*_}" == coc ]] && coc_step=2
			[[ $nerdtree_step -eq 1 && "${plug#*_}" == nerdtree ]] && nerdtree_step=2
		done
	fi
	[[ -n "$coc_block" ]] && echo -e "$coc_block" >> ../nvim/vim-plug.vim && coc_block=
	echo -e "$nerdtree_block" >> ../nvim/vim-plug.vim
done > /dev/stderr
cd ..
echo 'call plug#end()' >> nvim/vim-plug.vim
echo -e '\e[1;31mDone\e[0m'
[[ $coc_enabled == yes ]] && coc_extra="${coc_extra}]"
echo "$coc_extra" >> nvim/vim-plug.vim

unset pluginChanges

# Create colorscheme file
for scheme in ${schemes[@]}; do
	echo "$scheme" >> nvim/colorschemes.temp
done

# Install/Update
echo 'Installing vim-plug + new plugins...'
nvim -es -u nvim/init.vim -i NONE +qa <<< ""
echo 'Updating vim-plug...'
nvim -es -u nvim/init.vim -i NONE +PlugUpgrade +qa <<< ""
echo 'Cleaning plugins...'
nvim -es -u nvim/init.vim -i NONE +PlugClean! +qa! <<< "y"
echo 'Updating plugins...'
nvim -es -u nvim/init.vim -i NONE +PlugUpdate +qa <<< ""
