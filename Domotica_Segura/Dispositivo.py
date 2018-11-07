import json
import requests
import time
import ConfigParser as cp
import Constantes as ctes
            ######### DESCOMENTAR #########
#import Adafruit_DHT
#import RPi.GPIO as GPIO

import sys
import urllib2
from urllib2 import Request
import abc
from abc import ABCMeta

import sqlite3

##########################################################
# Clase
# Nombre: 
#   Dispositivo
# Descripcion:
#   Clase que define las funciones basicas que integran
#   un dispositivo.
# Tipo:
#   abstracta
# Atributos:
#   name, nombre del dispositivo HW
#   type, tipo del dispositivo
#   state, estado del dispositivo (Activo/Inactivo)
#   frecuencia, frecuencia de envio de informacion
#   gpio, pin de la RPi al que esta conectado
#   id_device, identificador del dispositivo
##########################################################
class Dispositivo:
    
    def __init__(self, name, type, state, frecuencia, gpio, id_device):
        self.nombre = name
        self.tipo = type
        self.estado = state
        self.pin = gpio
        self.freq = frecuencia
        self.id = id_device
        
    ############################################
    # Obtener ip externa de la RPi
    ############################################
    def obtener_ip(self):
        lista = "0123456789."
        ip=""
        dato=urllib2.urlopen("http://checkip.dyndns.org").read()
        for x in str(dato):
            if x in lista:
                ip += x
        return ip
    
    ##################################################
    # Conseguir el codigo de verificacion del cliente
    ##################################################
    def get_code_verify (self):

        file_config = ctes.FILE_WIFI_CONFIG
        if os.path.isfile(file_config):
            # Leer el archivo de configuracion:
            configuracion = cp.ConfigParser()
            configuracion.readfp(open(file_config))

            if 'SECURITY' in configuracion.sections():
                codeVerify = configuracion.get('SECURITY','VERIFY_CODE')
        return codeVerify
        

    #####################################################
    # Envio del comando inicial para establecer conexion
    #####################################################
    @abc.abstractmethod
    def iniciar_conexion(self):
        print("Enviamos peticion POST para conectarnos al servidor...")
        
    ######################################################
    # Envio de comandos para mantener la conexion abierta
    ######################################################
    @abc.abstractmethod
    def mantener_conexion(self):
        print("Enviamos peticiones PUT para mantener la conexion con el servidor...")
        
    ##########################################
    # Conseguir la informacion de dispositivo 
    ##########################################
    @abc.abstractmethod
    def obtener_informacion(self):
        print("Obtenemos la informacion actual para enviarla al servidor...")
    
    #############################################
    # Guardar los datos en la BBDD
    # Param:
    #   datos, datos a almacenar
    #############################################
    @abc.abstractmethod
    def guardar_datos(self, datos):
        print("guardamos los datos leidos del dispositivo...")
        

##############################################################
# Clase
# Nombre:
#   Sensor
# Descripcion:
#   Clase que implementa a la clase Dispositivo en modo Sensor
###############################################################
class Sensor(Dispositivo):
    
    def __init__(self, name, type, state, frecuencia, gpio):
        print("Ini SENSOR")
        self.nombre = name
        self.tipo = type
        self.estado = state
        self.pin = gpio
        self.freq = frecuencia
        self.id = -1
    
    def iniciar_conexion(self):
        print("Conecta SENSOR")
        condition = True
        ip = self.obtener_ip()
        #code = get_code_verify()
        while condition:
            print ("Esperando...")
            time.sleep(2)#Esperamos 2 segundos a recibir respuesta del servidor
            headers={'Content-type': 'application/json', 'dev-auth': 'bRm'}
            data_post = {"name" : self.nombre, "freq" : self.freq, "info" : "0", "IP": ip, "commands" : ["ON", "OFF", "+", "-"]}#, 'VeriFyCode':code}#tipo On/Off
            #url = 'http://localhost/devices.php'
            url = 'http://88.1.141.187:2999/brimo/api/devices'
            json_str = json.dumps(data_post)
            post = requests.post(url=url, headers=headers, data=json_str)#, cert('/etc/lighttpd/certs/lighttpd.pem'))
            print ("\n\n--- POST - Sensor ---")
            print ("\tEstado:\t", post.status_code)
            print ("\tTexto:\n",post.text)
            print ("\tDatos:\n",json_str)
            condition = (post.status_code != 201)
            
        # AQUI DEBO RECOGER EL ID ASIGNADO A ESTE SENSOR
        
        reply = post.json()
        self.id = reply['id']
        print ("\tID: ",self.id)
        
        #COMENTAR
        #self.id = 001
        
    def mantener_conexion(self):        
        #super(Dispositivo, self).mantiene()
        condition = True
        #code = get_code_verify()
        while condition:
            # ESPERAR TANTO TIEMPO COMO SE HAYA INDICADO EN EL POST ANTERIOR
            print ("Esperando...")
            time.sleep(self.freq)
            
            ######### DESCOMENTAR #########
            #datos = self.obtener_informacion()
            #temp, hum = datos
            #info = "Temperatura="+format(temp)+"*, Humedad="+format(hum)

            ######### COMENTAR #########
            info = "TEMPERATURA: x, HUMEDAD: y"

            if info != "ERROR":
                # ESTE JSON DEBERIA FORMARSE CON LOS DATOS RECOGIDOS DEL SENSOR
                headers={'Content-type': 'application/json', 'dev-auth': 'bRm'}
                data_put = {"id":self.id, "info":info}
                #url = 'http://localhost/devices.php'
                url = 'http://88.1.141.187:2999/brimo/api/devices/'+str(self.id)
                print ("URL",url)
                json_str = json.dumps(data_put)
                put = requests.put(url=url, headers=headers, data=json_str)#, cert('/etc/lighttpd/certs/lighttpd.pem'))
                print ("\n\n--- PUT- Sensor ---")
                print ("\tEstado:\t", put.status_code)
                #print ("\tTexto:\n",put.text)
                self.guardar_datos(info)
                condition = (put.status_code == 200)
            else:
                condition = False
                print ("[Error PUT] Error al crear el elemento JSON")
    
    def obtener_informacion(self):
        #super(Dispositivo, self).obtiene_informacion()
        # Configuracion del tipo de sensor DHT
        sensor = Adafruit_DHT.DHT11
        
        humedad, temperatura = Adafruit_DHT.read_retry(sensor, self.pin)
        
        #dummy - COMENTAR
        return 15, 20
        #return temperatura, humedad
    
    def guardar_datos(self, datos):
        
        fecha = time.strftime("%d%m%y")
        hora = time.strftime("%X")
        temperatura, humedad = datos

        print("Id: ", self.id,type(self.id))
        print("Fecha: ", fecha,type(fecha))
        print("Hora: ", hora, type(hora))
        print("Temperatura: ", temperatura, type(temperatura))
        print("Humedad: ", humedad, type(humedad))
        dat = "T: " + str(temperatura) + " - H: " + str(humedad)
        print("Dat: ", dat, type(dat))

        ###################### DESCOMENTAR ######################
        #conn = sqlite3.connect('/BBDD/devices_domotica.db')
        #cursor = conn.cursor()

        #query = "INSERT INTO data_device (id, nombre, tipo, fecha, hora, dato) VALUES (?,?,?,?,?,?)"
        #cursor.execute(query, (self.id, "Humedad y Temperatura", 'S', fecha, hora, dat))
        
        #conn.commit()
        #conn.close()

        print("[SENSOR] Insercion correcta.")

##############################################################
# Clase
# Nombre:
#   Actuador
# Descripcion:
#   Clase que implementa a la clase Dispositivo en modo Actuador
###############################################################
class Actuador(Dispositivo):
    
    def __init__(self, name, type, state, frecuencia, gpio):
        self.nombre = name
        self.tipo = type
        self.estado = state
        self.pin = gpio
        self.freq = frecuencia
        self.id = -1
            
    def prueba_borrar(self):#recojo de teclado si la activacion o desactivacion del rele
        print("INTRODUCIR On(1)/Off(0), PARA ACTIVAR O DESACTIVAR EL RELE: ")
        res = input()
        print(type(res))
        return res
        
    def ini_actuador(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        
    def activa_actuador(self):
        GPIO.output(self.pin, GPIO.HIGH)
        
    def desactiva_actuador(self):
        GPIO.output(self.pin, GPIO.LOW)        
    
    def iniciar_conexion(self):
        condition = True
        ip = self.obtener_ip()
        #code = get_code_verify()
        print(type(ip), ip)

        while condition:
            print ("Esperando...")
            time.sleep(2)            
            headers={'Content-type': 'application/json', 'dev-auth': 'bRm'}
            data_post = {"name" : self.nombre, "freq" : self.freq, "info" : "0", "IP": ip, "commands" : ["ON", "OFF", "+", "-"]}#, 'VeriFyCode':code}#tipo On/Off
            #url = 'http://localhost/devices.php'
            url = 'http://88.1.141.187:2999/brimo/api/devices'
            json_str = json.dumps(data_post)
            post = requests.post(url=url, headers=headers, data=json_str)#, cert('/etc/lighttpd/certs/lighttpd.pem'))
            print ("\n\n--- POST - Actuador ---")
            print ("\tEstado:\t", post.status_code)
            print ("\tTexto:\n",post.text)
            print ("\tDatos:\n",json_str)
            condition = (post.status_code != 201)
        
        #AQUI DEBO RECOGER EL ID ASIGNADO A ESTE SENSOR
        
        reply = post.json()
        self.id = reply['id']        
        print ("\tID: ",self.id)
        
        
        #dummy - COMENTAR
        #self.id = 002
        
    def mantener_conexion(self):
        condition = True
        #self.ini_actuador()
        #code = get_code_verify()
        while condition:
            # ESPERAR TANTO TIEMPO COMO SE HAYA INDICADO EN EL POST ANTERIOR
            print ("Esperando...")
            time.sleep(self.freq)
            
            # Recibo un post con la mi ip el json(id y la accion(ON/OF))

            ######### DESCOMENTAR #########
            # cada x tiempo (freq) enviar un put con la info necesaria
            
            #if self.prueba_borrar() == 1:
            #    self.activa_actuador()
            #else:
            #    self.desactiva_actuador()
            
            #estado = self.obtener_informacion()
            
            ######### dummy - COMENTAR #########
            estado = "ESTADO"

            headers={'Content-type': 'application/json', 'dev-auth': 'bRm'}
            data_put = {"id":self.id, "info":estado}
            #url = 'http://localhost/devices.php'
            url = 'http://88.1.141.187:2999/brimo/api/devices/'+str(self.id)
            json_str = json.dumps(data_put)
            put = requests.put(url=url, headers=headers, data=json_str)#, cert('/etc/lighttpd/certs/lighttpd.pem'))
            print ("\n\n--- PUT - Actuador ---")
            print ("\tEstado:\t", put.status_code)
            print ("\tTexto:\n",put.text)
            self.guardar_datos(estado)
            condition = (put.status_code == 200)
            #si no devuelve 200 enviar otra vez post ...
            
    def guardar_datos(self, datos):
        
        fecha = time.strftime("%d%m%y")
        hora = time.strftime("%X")
        
        print("Id: ", self.id, type(self.id))
        print("Fecha: ", fecha, type(fecha))
        print("Hora: ", hora, type(hora))
        print("Datos: ", datos, type(datos))
        

        ###################### DESCOMENTAR ######################
        #conn = sqlite3.connect('/BBDD/devices_domotica.db')
        #cursor = conn.cursor()

        #query = "INSERT INTO data_device (id, nombre, tipo, fecha, hora, dato) VALUES (?,?,?,?,?,?)"
        #cursor.execute(query, (self.id, "Rele", 'A', fecha, hora, datos))
        
        #conn.commit()
        #conn.close()
        print("[ACTUADOR] Insercion correcta.")
    
    def obtener_informacion(self):
        if GPIO.input(self.pin) == GPIO.LOW:
            return "Inactivo" #el rele esta desactivado
        else:
            return "Activo" #el rele esta activado
        
    
    
    
    
    
    
    
    