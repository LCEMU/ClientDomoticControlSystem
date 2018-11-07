import os
import Constantes as ctes

class ConfigAP():

    def __init__(self):
        self.fileAP = ctes.FILE_AP
        self.fileInterface = ctes.FILE_INTERFACES
        self.content = []


    ################################################################
    # Funcion
    # Nombre:
    #   get_estado_AP
    # Descripcion:
    #   Consigue el estado de la RPi, si actua como Access Point o no
    #################################################################
    def get_estado_AP(self):
        f = open(self.fileAP, "r")
        self.content = f.readlines()
        f.close()
                
        if ctes.FLAG_ON_AP in self.content:
            ctes.LOG = ctes.LOG +   ctes.hora + " File ConfigAP.py [INFO] - AP Activa\n"
            return True
        else:
            ctes.LOG = ctes.LOG +  ctes.hora + " File ConfigAP.py [INFO] - AP Inactiva\n"
            return False

    ################################################################
    # Funcion
    # Nombre:
    #   onAP
    # Descripcion:
    #   Activa la RPi como Access Point
    #################################################################
    def onAP(self):
        if self.get_estado_AP() == False:
            self.content = ctes.remove_lines(self.content, ctes.FLAG_OFF_AP, 1)
            f = open(self.fileAP, "w")
            for linea in self.content:
                f.write(linea)
            f.write(ctes.FLAG_ON_AP)
            f.write("# IP ESTATICA (CODIGO QUE ACTIVA EL Access Point)\n")
            f.write("interface wlan0\n")
            f.write("static ip_address=192.168.4.1/24\n")
            f.write("nohook wpa_supplicant\n")
            ctes.LOG = ctes.LOG + ctes.hora + " File ConfigAP.py [OK] - ON\n"
            f.close()
        else:
            ctes.LOG = ctes.LOG + ctes.hora + " File ConfigAP.py [ERROR] - ON\n"
            
    ################################################################
    # Funcion
    # Nombre:
    #   offAP
    # Descripcion:
    #   Desactiva la RPi como Access Point
    #################################################################
    def offAP(self):
                
        if self.get_estado_AP() == True:
            self.content =  ctes.remove_lines(self.content, ctes.FLAG_ON_AP, ctes.NUM_LIN_STATIC_IP)
            f = open(self.fileAP, "w")
            for linea in self.content:
                f.write(linea)
            f.write(ctes.FLAG_OFF_AP)
            f.close()
            ctes.LOG = ctes.LOG +ctes.hora + " File ConfigAP.py [OK] - OFF\n"
        else:
            ctes.LOG = ctes.LOG + ctes.hora + " File ConfigAP.py [ERROR] - OFF\n"
