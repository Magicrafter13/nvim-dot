" Integrate with system clipboard (KDE's Klipper)
let g:clipboard = {
	\   'name': 'klipper',
	\   'copy': {
	\     '+': 'klipperCopy 2> ~/klipper.log',
	\     '*': 'klipperCopy > ~/klipper.log',
	\   },
	\   'paste': {
	\     '+': 'qdbus org.kde.klipper /klipper getClipboardContents',
	\     '*': 'qdbus org.kde.klipper /klipper getClipboardContents',
	\   },
	\ }
