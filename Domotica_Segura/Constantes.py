#!/usr/bin/python

##############################################################
# Fichero
# Nombre:
#   Constantes.py
# Descripcion:
#   Define todas las constantes y las funciones auxiliares
#   del sistema
###############################################################
import time

LOG = ""
fecha = time.strftime("%d%m%y")
hora = time.strftime("%X")

#CONSTANTES
NUM_LIN_STATIC_IP = 5 # numero de lineas que configuran la ip estatica en /etc/dhcpcd.conf para activar el AP
NUM_LIN_WIFI_CONFIG = 10 # numero de lineas que configuran la conexxion wifi en /etc/network/interfaces

OK = 0
ERR = -1

IP = "88.1.141.187:2999"

FILE_AP = "/etc/dhcpcd.conf"
FILE_INTERFACES = "/etc/network/interfaces"
FILE_WIFI_CONFIG = "/var/www/html/Register/WifiConnect.cfg"
FILE_LOG = "/home/pi/Desktop/Domotica_Segura/Log/DomoticSystem"+fecha+".log"

FLAG_ON_AP = "#AP_ACTIVA\n"
FLAG_OFF_AP = "#AP_DESACTIVADA\n"
FLAG_WIFI_CONFIG = "## Configuracion Wifi ##\n"
FLAG_NO_WIFI_CONFIG = "## Wifi No configurado ##\n"

##############################################################
# Funcion
# Nombre:
#   get_content_file
# Descripcion:
#   Consigue el contenido de un fichero
# Param:
#   file, fichero del cual queremos conseguir el contenido
###############################################################
def get_content_file (file):
    f = open(file, "r")
    content = f.readlines()
    f.close()
    return content

#################################################################
# Funcion
# Nombre:
#   get_lines_file
# Descripcion:
#   Consigue el numero de lineas de una fichero
# Param:
#   file, fichero del cual queremos conseguir el numero de lineas
##################################################################
def get_lines_file(file):
    f = open(file, "r")
    lines = len(f.readlines())
    f.close()
    return lines

def add_to_file(file, cad):
    f = open(file, "a")
    f.write(cad)
    f.close()

#####################################################
# Funcion
# Nombre:
#   remove_lines
# Descripcion:
#   Borra todos tantos registros como indique <numLines> desde la posision <indexIni>
# Param:
#   indexIni : indice desde el cual se comienza a borrar
#   numLines : numero de registros que queremos borrar
#####################################################
def remove_lines (lista, word, numLines):
    indexIni = lista.index(word)
    indexFin = indexIni + numLines
    if numLines > 1:
        rang = list(range(indexIni, indexFin))
        # invertimos el orden del rango para no tener problemas al borrar las lineas
        rang.reverse()
        for i in rang:
            lista.pop(i)
    else:
        lista.pop(indexIni)
    return lista
