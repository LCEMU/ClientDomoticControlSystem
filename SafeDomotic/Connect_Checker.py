import os
import commands
import ConfigAP
import Constantes as ctes
import time


##############################################################
# Funcion
# Nombre:
#   comprobarConexion
# Descripcion:
#   Comprueba si la RPi esta conextada al wifi correctamente
###############################################################
def comprobarConexion():
    wlan0=commands.getoutput('ifconfig wlan0')
    wlan0 = wlan0.split(' ')
    count=0
    if "inet" in wlan0:
        for i in wlan0:
            if i=="inet":
                break
            count += 1
        print(wlan0[count+1])
        ctes.LOG = ctes.LOG + str(wlan0[count+1])
        return ctes.OK
    else:
        return ctes.ERR

################################################################
# Funcion
# Nombre:
#   delete_credentials
# Descripcion:
#   Elimina las credenciales del fichero /etc/network/interfaces
#################################################################
def delete_credentials():

    content = ctes.get_content_file(ctes.FILE_INTERFACES)

    if ctes.FLAG_WIFI_CONFIG in content:
        content = ctes.remove_lines (content, ctes.FLAG_WIFI_CONFIG, ctes.NUM_LIN_WIFI_CONFIG)
        for linea in content:
            f.write(linea)
        f = open(ctes.FILE_INTERFACES, "w")
        f.write(ctes.FLAG_NO_WIFI_CONFIG)
        f.close()
    else:
        ctes.LOG = ctes.LOG + ctes.hora + " Connect_Checker.py [ERROR] No existe la cadena "+ctes.FLAG_WIFI_CONFIG+" en "+ctes.FILE_INTERFACES+"\n"

## MAIN ##
if __name__ == '__main__':
    #Esperamos 10 segundos para que la rpi acabe de iniciarse y luego comprobamos la conexion
    #time.sleep(10)
    cap = ConfigAP.ConfigAP()

    #Comprobamos si tenemos una IP asignada, es decir, si estamos conectados a algun wifi
    conn = comprobarConexion()

    #Comprobamos si la AP esta activa
    if conn == ctes.ERR and cap.get_estado_AP() == False:
        on = ConfigAP.ConfigAP()
        delete_credentials()
        on.onAP()
        ctes.LOG = ctes.LOG + ctes.hora + "File Connect_Checker.py [INFO] REBOOT: por credenciales erroneas\n"
        #os.system('reboot')
    else:
        ctes.LOG = ctes.LOG + ctes.hora + "File Connect_Checker.py [INFO] NO REBOOT: credenciales correctas\n"

    ctes.add_to_file(ctes.FILE_LOG, ctes.LOG)
