#coding=utf-8
friendly_name={
    'Up': '↑', 'Down': '↓', 'Left': '←', 'Right': '→',
    'Return': 'Enter', 'Space': '⎵', 'Cancel': 'Break', 'Back': '⌫', 'Delete': 'Del',
    'Capital': 'CapsLk', 'Scroll': 'ScrLk', 'Apps': 'Menu',
    'Escape': 'Esc', 'Snapshot': 'PrtSc', 'Prior': 'PgUp', 'Next': 'PgDn',
    'Lcontrol': 'Ctrl', 'Lmenu': 'Alt', 'Lwin': 'Win', 'Lshift': 'Shift',
    'Rcontrol': 'Ctrl(R)', 'Rmenu': 'Alt(R)', 'Rwin': 'Win(R)', 'Rshift': 'Shift(R)',
    'Oem_Minus': '-', 'Oem_Plus': '=',  'Oem_Comma': ',', 'Oem_Period': '.',
    'Oem_5': '\\', 'Oem_3': '`', 'Oem_2': '/', 'Oem_1': ';', 'Oem_7': "'", 'Oem_4': '[', 'Oem_6': ']',
    'Volume_Mute': 'Mute', 'Volume_Up': 'Vol+', 'Volume_Down': 'Vol-',
}
for n in range(10):
    friendly_name['Numpad%d'%n]='Num %d'%n

mouse_evt_name={
    'mouse left down': [True,0],
    'mouse left up': [False,0],
    'mouse middle down': [True,1],
    'mouse middle up': [False,1],
    'mouse right down': [True,2],
    'mouse right up': [False,2],
}
tip_format='%H:%M:%S '
print_log=False