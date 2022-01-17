" Integrate with system clipboard (KDE's Klipper)
let g:clipboard = {
	\   'name': 'klipper',
	\   'copy': {
	\     '+': 'klipperCopy',
	\     '*': 'xclip -i',
	\   },
	\   'paste': {
	\     '+': 'qdbus org.kde.klipper /klipper getClipboardContents',
	\     '*': 'xclip -o',
	\   },
	\ }
