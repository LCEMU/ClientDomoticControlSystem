import os
import os.path
import commands
import Constantes as ctes
import ConfigAP
import ConfigParser as cp

##############################################################
# Function
# Nombre:
#   save_credentials
# Descripcion:
#   Rellena el fichero /etc/network/interfaces con las
#   credenciales introducidas por el usuario.
# Param:
#   name, nombre de la red wifi
#   psw, password de la red wifi
###############################################################
def save_credentials(name, psw):
    
    content = ctes.get_content_file(ctes.FILE_INTERFACES)
    print content
    print ctes.FLAG_NO_WIFI_CONFIG
    
    if ctes.FLAG_NO_WIFI_CONFIG in content:
        content = ctes.remove_lines (content, ctes.FLAG_NO_WIFI_CONFIG, 1)
        f = open(ctes.FILE_INTERFACES, "w")    
        for linea in content:
            f.write(linea)
        f.write(ctes.FLAG_WIFI_CONFIG)
        f.write("auto lo\n")
        f.write("iface lo inet loopback\n")
        f.write("iface eth0 inet dhcp\n")
        f.write("allow-hotplug wlan0\n")
        f.write("auto wlan0\n")
        f.write("iface wlan0 inet dhcp\n")
        f.write('\twpa-ssid "'+name+'"\n')
        f.write('\twpa-psk "'+psw+'"\n')
        f.write("################\n")
        f.close()
        
        ctes.LOG = ctes.LOG +ctes.hora + " File Wifi_Checker.py [OK] Credenciales en /etc/network/interfaces\n"
        
    else:
        ctes.LOG = ctes.LOG +ctes.hora + " File Wifi_Checker.py [ERROR] Credenciales erroneas o inexistentes en /etc/network/interfaces\n"

if __name__ == '__main__':    
    #Comprobamos si el sistema se ha iniciado como AP
    #    Si es asi dejamos de ejecutar este script
    #    Si no es asi seguimos ejecutando
    
    ap = ConfigAP.ConfigAP()
    
    #Comprobamos si el modo Access Point esta desactivado
    if ap.get_estado_AP() == False:
        ctes.LOG = ctes.hora + " File Wifi_Checker.py [OK] AP en estado OFF\n"

        file_config = ctes.FILE_WIFI_CONFIG
        if os.path.isfile(file_config):
            # Conectar a la wifi
            ctes.LOG = ctes.LOG + ctes.hora + " File Wifi_Checker.py [OK] Fichero "+ file_config +"encontrado\n"

            # Leer el archivo de configuracion:
            configuracion = cp.ConfigParser()
            configuracion.readfp(open(file_config))
            
            for seccion in configuracion.sections():
                ctes.LOG = ctes.LOG + ctes.hora + " File Wifi_Checker.py [INFO]"+seccion+"\n"
                
            ctes.LOG = ctes.LOG + ctes.hora + " File Wifi_Checker.py [OK] Leer fichero de configuracion\n"

            if 'WIFI' in configuracion.sections() or 'SECURITY' in configuracion.sections():
                nombreWifi = configuracion.get('WIFI','NOMBRE')
                passWifi = configuracion.get('WIFI','PASSWORD')
                codeVerify = configuracion.get('SECURITY','VERIFY_CODE')
                ctes.LOG = ctes.LOG + ctes.hora + " File Wifi_Checker.py [OK] Credenciales configuradas\n"

                ##FUNCION PARA CONECTAR AL WIFI
                save_credentials(nombreWifi, passWifi)
                
            else:
                ctes.LOG = ctes.LOG + '[ERROR] Formato de fichero incorrecto\n'
        else:
            ctes.LOG = ctes.LOG + ctes.hora + " File Wifi_Checker.py [ERROR] El fichero "+ file_config +" no existe\n"
    else:
        ctes.LOG = ctes.LOG + ctes.hora + " File Wifi_Checker.py [ERROR] AP en estado ON\n"

    ctes.add_to_file(ctes.FILE_LOG, ctes.LOG)