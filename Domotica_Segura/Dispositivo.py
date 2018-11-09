import os
import json
import requests
import time
import ConfigParser as cp
import Constantes as ctes
            ######### DESCOMENTAR #########
import Adafruit_DHT
import RPi.GPIO as GPIO

import sys
import urllib2
from urllib2 import Request
import abc
from abc import ABCMeta

import sqlite3

##########################################################
# Clase
# Nombre:
#   Device
# Descripcion:
#   Clase que define las funciones basicas que integran
#   un device.
# Tipo:
#   abstracta
# Atributos:
#   sName, nombre del device HW
#   sType, tipo del dispositivo
#   sState, state del dispositivo (Activo/Inactivo)
#   sFreq, frecuencia de envio de informacion
#   sGpio, pin de la RPi al que esta conectado
#   id_device, identificador del dispositivo
##########################################################
class Device:

    def __init__(self, sName, sType, sState, sFreq, sGpio, id_device):
        self.name = sName
        self.type = sType
        self.state = sState
        self.pin = sGpio
        self.freq = sFreq
        self.id = id_device

    ############################################
    # Obtener ip externa de la RPi
    ############################################
    def get_ip(self):
        liist = "0123456789."
        ip=""
        data=urllib2.urlopen("http://checkip.dyndns.org").read()
        for x in str(data):
            if x in liist:
                ip += x
        return ip

    ##################################################
    # Conseguir el codigo de verificacion del cliente
    ##################################################
    def get_code_verify (self):

        ############# DESCOMENTAR ##############
        file_config = ctes.FILE_WIFI_CONFIG
        if os.path.isfile(file_config):
            # Leer el archivo de configuracion:
            configuracion = cp.ConfigParser()
            configuracion.readfp(open(file_config))

            if 'SECURITY' in configuracion.sections():
                codeVerify = configuracion.get('SECURITY','VERIFY_CODE')

        return codeVerify

        ################## COMENTAR ##################
        #return 'bRm'


    #####################################################
    # Envio del comando inicial para establecer conexion
    #####################################################
    @abc.abstractmethod
    def start_connection(self):
        print("Enviamos peticion POST para conectarnos al servidor...")

    ######################################################
    # Envio de comandos para mantener la conexion abierta
    ######################################################
    @abc.abstractmethod
    def keep_connection(self):
        print("Enviamos peticiones PUT para mantener la conexion con el servidor...")

    ##########################################
    # Conseguir la informacion de dispositivo
    ##########################################
    @abc.abstractmethod
    def get_info(self):
        print("Obtenemos la informacion actual para enviarla al servidor...")

    #############################################
    # Guardar los data en la BBDD
    # Param:
    #   data, data a almacenar
    #############################################
    @abc.abstractmethod
    def save_data(self, data):
        print("guardamos los data leidos del device...")


##############################################################
# Clase
# Nombre:
#   Sensor
# Descripcion:
#   Clase que implementa a la clase Device en modo Sensor
###############################################################
class Sensor(Device):

    def __init__(self, sName, sType, sState, sFreq, sGpio):
        print("Ini SENSOR")
        self.name = sName
        self.type = sType
        self.state = sState
        self.pin = sGpio
        self.freq = sFreq
        self.id = -1
        self.code = ""

    def start_connection(self):
        print("Conecta SENSOR")
        condition = True
        ip = self.get_ip()
        self.code = self.get_code_verify()

        while condition:
            print ("Esperando...")
            time.sleep(2)#Esperamos 2 segundos a recibir respuesta del servidor
            headers={'Content-type': 'application/json', 'dev-auth': self.code}
            data_post = {"name" : self.name, "freq" : self.freq, "info" : "0", "IP": ip, "commands" : ["ON", "OFF", "+", "-"]}
            #url = 'http://localhost/devices.php'
            url = 'http://88.1.141.187:2999/brimo/api/devices'
            json_str = json.dumps(data_post)
            post = requests.post(url=url, headers=headers, data=json_str)#, cert('/etc/lighttpd/certs/lighttpd.pem'))
            print ("\n\n--- POST - Sensor ---")
            print ("\tEstado:\t", post.status_code)
            condition = (post.status_code != 201)

        # AQUI DEBO RECOGER EL ID ASIGNADO A ESTE SENSOR
        reply = post.json()
        self.id = reply['id']
        print ("\tID: ",self.id)

    def keep_connection(self):
        condition = True

	conn = sqlite3.connect('./BBDD/devices_domotica.db')
        cursor = conn.cursor()
        name = 'S'+str(self.pin)

        query = "INSERT INTO device(id, pin, name, type) VALUES (?,?,?,?)"
        cursor.execute(query, (self.id, self.pin, name, 'S'))

        conn.commit()
        conn.close()

        while condition:
            # ESPERAR TANTO TIEMPO COMO SE HAYA INDICADO EN EL POST ANTERIOR
            print ("Esperando...")
            time.sleep(self.freq)

            ######### DESCOMENTAR #########
            data = self.get_info()
            temp, hum = data
            info = "Temperatura="+format(temp)+"*, Humedad="+format(hum)

            if info != "ERROR":
                # ESTE JSON DEBERIA FORMARSE CON LOS DATOS RECOGIDOS DEL SENSOR
                headers={'Content-type': 'application/json', 'dev-auth': 'bRm'}
                data_put = {"id":self.id, "info":info}
                #url = 'http://localhost/devices.php'
                url = 'http://88.1.141.187:2999/brimo/api/devices/'+str(self.id)
                json_str = json.dumps(data_put)
                put = requests.put(url=url, headers=headers, data=json_str)#, cert('/etc/lighttpd/certs/lighttpd.pem'))
                print ("\n\n--- PUT- Sensor ---")
                print ("\tEstado:\t", put.status_code)
                self.save_data(data)
                condition = (put.status_code == 200)
            else:
                condition = False
                print ("[Error PUT] Error al crear el elemento JSON")

    def get_info(self):

        # Configuracion del tipo de sensor DHT
        ####################### DESCOMENTAR #####################
        sensor = Adafruit_DHT.DHT11
        humidity, temp = Adafruit_DHT.read_retry(sensor, self.pin)

        ######### DUMMY - COMENTAR ###########
        #return 15, 20
        return temp, humidity

    def save_data(self, data):

        date = time.strftime("%d/%m/%Y")
        ttime = time.strftime("%X")
        print data
        temp, humidity = data

        print("Id: ", self.id,type(self.id))
        dat = "T: " + str(temp) + " - H: " + str(humidity)

        ###################### DESCOMENTAR ######################
        conn = sqlite3.connect('./BBDD/devices_domotica.db')
        cursor = conn.cursor()

        query = "INSERT INTO activity_device (id, ddate, time, info) VALUES (?,?,?,?)"
        cursor.execute(query, (self.id, date, ttime, dat))

        conn.commit()
        conn.close()

        print("[SENSOR] Insercion correcta.")

##############################################################
# Clase
# Nombre:
#   Actuador
# Descripcion:
#   Clase que implementa a la clase Device en modo Actuador
###############################################################
class Actuador(Device):

    def __init__(self, sName, sType, sState, sFreq, sGpio):
        self.name = sName
        self.type = sType
        self.state = sState
        self.pin = sGpio
        self.freq = sFreq
        self.id = -1
        self.code = ""

    def start_connection(self):
        condition = True
        ip = self.get_ip()
        self.code = self.get_code_verify()

        while condition:
            print ("Esperando...")
            time.sleep(2)
            headers={'Content-type': 'application/json', 'dev-auth': self.code}
            data_post = {"name" : self.name, "freq" : self.freq, "info" : "0", "IP": ip, "commands" : ["ON", "OFF", "+", "-"]}
            #url = 'http://localhost/devices.php'
            url = 'http://88.1.141.187:2999/brimo/api/devices'
            json_str = json.dumps(data_post)
            post = requests.post(url=url, headers=headers, data=json_str)#, cert('/etc/lighttpd/certs/lighttpd.pem'))
            print ("\n\n--- POST - Actuador ---")
            print ("\tEstado:\t", post.status_code)
            print ("\tTexto:\n",post.text)
            print ("\tDatos:\n",json_str)
            condition = (post.status_code != 201)

        #AQUI DEBO RECOGER EL ID ASIGNADO A ESTE ACTUADOR
        reply = post.json()
	self.id = reply['id']
        print ("\tID: ",self.id)

    def keep_connection(self):
        condition = True

        conn = sqlite3.connect('./BBDD/devices_domotica.db')
        cursor = conn.cursor()
        name = 'A'+str(self.pin)

        query = "INSERT INTO device(id, pin, name, type) VALUES (?,?,?,?)"
        cursor.execute(query, (self.id, self.pin, name, 'A'))

        conn.commit()
        conn.close()

        try:
            while condition:
                # ESPERAR TANTO TIEMPO COMO SE HAYA INDICADO EN EL POST ANTERIOR
                print ("Esperando...")
                time.sleep(self.freq)

                state = self.get_info()

                headers={'Content-type': 'application/json', 'dev-auth': 'bRm'}
                data_put = {"id":self.id, "info":state}
                #url = 'http://localhost/devices.php'
                url = 'http://88.1.141.187:2999/brimo/api/devices/'+str(self.id)
                json_str = json.dumps(data_put)
                put = requests.put(url=url, headers=headers, data=json_str)#, cert('/etc/lighttpd/certs/lighttpd.pem'))

                print ("\n\n--- PUT - Actuador ---")
                print ("\tEstado:\t", put.status_code)

                self.save_data(state)
                condition = (put.status_code == 200)
                #si no devuelve 200 enviar otra vez post ...

        except KeyboardInterrupt:
            GPIO.cleanup()

    def save_data(self, data):

        date = time.strftime("%d/%m/%Y")
        ttime = time.strftime("%X")

        print("Id: ", self.id, type(self.id))

        ###################### DESCOMENTAR ######################
        conn = sqlite3.connect('./BBDD/devices_domotica.db')
        cursor = conn.cursor()

        query = "INSERT INTO activity_device (id, ddate, time, info) VALUES (?,?,?,?)"
        cursor.execute(query, (self.id, date, ttime, data))

        conn.commit()
        conn.close()

        print("[ACTUADOR] Insercion correcta.")

    def get_info(self):
	GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        if GPIO.input(self.pin) == GPIO.LOW:
            return "Inactivo" #el rele esta desactivado
        else:
            return "Activo" #el rele esta activado
