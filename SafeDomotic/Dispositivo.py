import os
import json
import requests
import time
import ConfigParser as cp
import Constantes as ctes

import Adafruit_DHT
import RPi.GPIO as GPIO

import sys
import urllib2
from urllib2 import Request
import abc
from abc import ABCMeta
import subprocess
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
    # Obtener ip publica
    ############################################
    def get_public_ip_net(self):
        liist = "0123456789."
        ip=""
        data=urllib2.urlopen("http://checkip.dyndns.org").read()
        for x in str(data):
            if x in liist:
                ip += x
        ctes.LOG = ctes.LOG + ctes.hora + "File Dispositivo.py [INFO] Public IP: \n" + ip
        return ip

    ############################################
    # Obtener ip de la subred
    ############################################
    def get_ip_subnet(self):
        wlan0 = subprocess.check_output('ifconfig wlan0 | grep "inet "', shell=True)
        wlan0 = wlan0.split()
        wlan0_map = map(lambda x: x.decode('UTF-8'), wlan0)
        count=0
        if "inet" in wlan0_map:
            ip = wlan0[1].decode('UTF-8')
            ctes.LOG = ctes.LOG + ctes.hora + "File Dispositivo.py [INFO] Subnet IP: " + ip +"/n"
            return ip
        else:
            ctes.LOG = ctes.LOG + ctes.hora + "File Dispositivo.py [ERR] get_ip_subnet\n"
            return ctes.ERR

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
        ip = self.get_public_ip_net()
        ip_subnet = self.get_ip_subnet()
        self.code = self.get_code_verify()

        while condition:
            print ("Esperando...")
            time.sleep(2)#Esperamos 2 segundos a recibir respuesta del servidor
            headers={'Content-type': 'application/json', 'dev-auth': self.code}
            data_post = {"name" : self.name, "freq" : self.freq, "info" : "0", "IP": ip, "IPsubnet" : ip_subnet, "commands" : ["ON", "OFF", "+", "-"]}
            #url = 'http://localhost/devices.php'
            url = 'http://88.1.141.187:3000/brimo/api/devices'
            json_str = json.dumps(data_post)
            post = requests.post(url=url, headers=headers, data=json_str, cert=('./SSL/client1-crt.pem', './SSL/client1-key.pem'))
            print ("\n\n--- POST - Sensor ---")
            ctes.LOG = ctes.LOG + ctes.hora + "File Dispositivo.py [INFO] Json Post Sensor:"+json_str+"/nStatus: "+str(post.status_code)+"/n"
            condition = (post.status_code != 201)

        # AQUI DEBO RECOGER EL ID ASIGNADO A ESTE SENSOR
        reply = post.json()
        self.id = reply['id']
        ctes.LOG = ctes.LOG + ctes.hora + "File Dispositivo.py [INFO] Id Sensor: "+str(self.id)+"/n"

    def keep_connection(self):
        condition = True

        conn = sqlite3.connect('./BBDD/DomoticControlSystem.db')
        cursor = conn.cursor()
        name = 'S'+str(self.pin)

        query = "INSERT INTO device(id, pin, name, type) VALUES (?,?,?,?)"
        cursor.execute(query, (self.id, self.pin, name, 'S'))

        conn.commit()
        conn.close()

        while condition:
            print ("Esperando...")
            time.sleep(self.freq)

            data = self.get_info()
            temp, hum = data
            info = "Temperatura="+format(temp)+"*, Humedad="+format(hum)

            if info != "ERROR":
                headers={'Content-type': 'application/json', 'dev-auth': 'bRm'}
                data_put = {"id":self.id, "info":info}
                url = 'http://88.1.141.187:3000/brimo/api/devices/'+str(self.id)
                json_str = json.dumps(data_put)
                put = requests.put(url=url, headers=headers, data=json_str, cert=('./SSL/client1-crt.pem', './SSL/client1-key.pem'))
                print ("\n\n--- PUT- Sensor ---")
                ctes.LOG = ctes.LOG + ctes.hora + "File Dispositivo.py [INFO] Json Put Sensor:"+json_str+"/nStatus: "+str(put.status_code)+"/n"
                self.save_data(data)
                condition = (put.status_code == 200)
            else:
                condition = False
                print ("[Error PUT] Error al crear el elemento JSON")

    def get_info(self):
        # Configuracion del tipo de sensor DHT
        sensor = Adafruit_DHT.DHT11
        humidity, temp = Adafruit_DHT.read_retry(sensor, self.pin)
        return temp, humidity

    def save_data(self, data):

        date = time.strftime("%d/%m/%Y")
        ttime = time.strftime("%X")
        temp, humidity = data
        dat = "T: " + str(temp) + " - H: " + str(humidity)

        conn = sqlite3.connect('./BBDD/DomoticControlSystem.db')
        cursor = conn.cursor()

        query = "INSERT INTO activity_device (id, ddate, time, info) VALUES (?,?,?,?)"
        cursor.execute(query, (self.id, date, ttime, dat))

        conn.commit()
        conn.close()

        ctes.LOG = ctes.LOG + ctes.hora + "File Dispositivo.py [INFO] SENSOR Insercion correcta./n-"

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
        ip = self.get_public_ip_net()
        ip_subnet = self.get_ip_subnet()
        self.code = self.get_code_verify()

        while condition:
            print ("Esperando...")
            time.sleep(2)
            headers={'Content-type': 'application/json', 'dev-auth': self.code}
            data_post = {"name" : self.name, "freq" : self.freq, "info" : "0", "IP": ip, "IPsubnet" : ip_subnet, "commands" : ["ON", "OFF", "+", "-"]}
            url = 'http://88.1.141.187:3000/brimo/api/devices'
            json_str = json.dumps(data_post)
            post = requests.post(url=url, headers=headers, data=json_str, cert=('./SSL/client1-crt.pem', './SSL/client1-key.pem'))
            print ("\n\n--- POST - Actuator ---")
            ctes.LOG = ctes.LOG + ctes.hora + "File Dispositivo.py [INFO] Json Post Sensor:"+json_str+"/nStatus: "+str(post.status_code)+"/n"
            condition = (post.status_code != 201)

        #AQUI DEBO RECOGER EL ID ASIGNADO A ESTE ACTUADOR
        reply = post.json()
        self.id = reply['id']
        ctes.LOG = ctes.LOG + ctes.hora + "File Dispositivo.py [INFO] Id Sensor: "+str(self.id)+"/n"

    def keep_connection(self):
        condition = True

        conn = sqlite3.connect('./BBDD/DomoticControlSystem.db')
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
                url = 'http://88.1.141.187:3000/brimo/api/devices/'+str(self.id)
                json_str = json.dumps(data_put)
                put = requests.put(url=url, headers=headers, data=json_str, cert=('./SSL/client1-crt.pem', './SSL/client1-key.pem'))
                print ("\n\n--- PUT - Actuador ---")
                ctes.LOG = ctes.LOG + ctes.hora + "File Dispositivo.py [INFO] Json Put Sensor:"+json_str+"/nStatus: "+str(put.status_code)+"/n"

                self.save_data(state)
                condition = (put.status_code == 200)
                #si no devuelve 200 enviar otra vez post ...

        except KeyboardInterrupt:
            GPIO.cleanup()

    def save_data(self, data):

        date = time.strftime("%d/%m/%Y")
        ttime = time.strftime("%X")

        conn = sqlite3.connect('./BBDD/DomoticControlSystem.db')
        cursor = conn.cursor()

        query = "INSERT INTO activity_device (id, ddate, time, info) VALUES (?,?,?,?)"
        cursor.execute(query, (self.id, date, ttime, data))

        conn.commit()
        conn.close()

        ctes.LOG = ctes.LOG + ctes.hora + "File Dispositivo.py [INFO] ACTUADOR Insercion correcta./n-"

    def get_info(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        if GPIO.input(self.pin) == GPIO.LOW:
            return "Disable" #el rele esta desactivado
        else:
            return "Enable" #el rele esta activado
