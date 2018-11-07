import commands

wlan0=commands.getoutput('ifconfig wlan0')
wlan0 = wlan0.split(' ')
count=0
if "inet" in wlan0:
    for i in wlan0:
        if i=="inet":
            break
        count += 1
    #print(wlan0[count+1])
    return "OK"
else:
    return "ERR"
