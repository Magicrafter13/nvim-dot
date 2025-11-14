#!/usr/bin/env bash

good=yes

for exe in python3 bash
do
	if ! command -v $exe >/dev/null
	then
		echo $exe executable not found
		good=no
	fi
done

if ! command -v cc >/dev/null
then
	echo "No C compiler found. Treesitter will not work!"
fi

if [ $good == no ]
then
	exit 1
fi

exit 0
