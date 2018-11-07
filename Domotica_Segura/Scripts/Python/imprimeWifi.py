from wifi import Cell
cells = Cell.all('wlan0')
wifis = ''
for cell in cells:
    wifis = wifis + cell.ssid + " "
    
print (wifis)