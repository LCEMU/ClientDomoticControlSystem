from http.server import BaseHTTPRequestHandler, HTTPServer
import simplejson as json
#import RPi.GPIO as GPIO
import numpy as np
import time
import sqlite3

class myHandler(BaseHTTPRequestHandler):
        
    ##########################################################################
    # Configuramos el modo de distribucion de los GPIO de la RPi y establecemos
    #  el 'pin' del dispositivo como salida
    # Param:
    #   pin, GPIO al cual esta conectado el actuador
    ##########################################################################
    def config_RPi(self, pin):
        '''
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        '''
        return "------> Ini actuador"


    ##########################################################################
    # Activamos el GPIO que indica 'pin' al cual esta conectado el actuador
    # Param:
    #   pin, GPIO al cual esta conectado el actuador
    ##########################################################################
    def activate_actuator(self, pin):
        '''
        self.config_RPi()
        GPIO.output(pin, GPIO.HIGH)
        '''
        return "------> Activar actuador"
        

    ##########################################################################
    # Desactivamos el GPIO que indica 'pin' al cual esta conectado el actuador
    # Param:
    #   pin, GPIO al cual esta conectado el actuador
    ##########################################################################
    def desactivate_actuator(self, pin):
        '''
        self.config_RPi()
        GPIO.output(pin, GPIO.LOW)
        '''
        return "------> Desactivar actuador"

    #############################################################
    # Guardar los data en la BBDD
    # Param:
    #   id_device, dispositivo sobre el que se realiza la accion
    #   data, informacion a almacenar
    #############################################################
    def save_action(self, id_device, data):

        date = time.strftime("%d/%m/%Y")
        ttime = time.strftime("%X")

        conn = sqlite3.connect('./BBDD/devices_domotica.db')
        cursor = conn.cursor()

        query = "INSERT INTO activity_device (id, ddate, time, info) VALUES (?,?,?,?)"
        cursor.execute(query, (id_device, date, ttime, data))
        
        conn.commit()
        conn.close()
        
        print("[ACTUADOR] Insercion correcta.")


    ###############################################################
    # Recogemos las peticiones POST del cliente y si los datos del
    #  mensaje son correctoslos registramos en la bbdd y devolvemos
    #  un 200 OK si no devolvemos un 400 o un 403 dependiendo del 
    #  tipo de error
    ###############################################################
    def do_POST(self):

        flag_response = 0

        print(">>> Recibo POST <<<")
        print("[[ A - CONTENT-LENGTH ]]: ",self.headers.get('content-length'))
        length = int(self.headers.get('content-length'))
        post_body = self.rfile.read(length)

        print("[[ BODY ]]\n",post_body.decode('UTF-8'))

        json_in = json.loads(post_body)

        if "Id" in json_in and "Action" in json_in:
            flag_response += 1
        else:
            self.send_response(400)
            self.send_header('Content-type','application/json')
            self.end_headers()
            return

        print("{}".format(json_in))
        id_device = json_in["Id"]
        action = json_in["Action"]
        print("ID: ",id_device)
        print("ACTION: ",action)
        print(json_in["Action"] == "On")

        conn = sqlite3.connect('./BBDD/devices_domotica.db')
        cursor = conn.cursor()

        query = "SELECT pin, type FROM device WHERE id=?"
        cursor.execute(query, (id_device,))

        row = cursor.fetchone()

        pin = row[0]
        print ("PIN: ", pin)
        dev_type = row[1]
        print ("TIPO: ", dev_type)
        
        conn.commit()
        conn.close()
        

        #Seleccionamos el nombre 
        ### print("DATA\n", data)
        ### dat = data[data[:,0]==id]
        ### print("SELECT: ", dat.decode())

        if dev_type == 'A' and flag_response > 0:

            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()

            if json_in["Action"] == "On":
                #Encender led
                self.activate_actuator(pin)
                self.save_action(id_device, "Enable")
                print("Encender led")
            else:
                #Apagar led
                self.desactivate_actuator(pin)
                self.save_action(id_device, "Disable")
                print("Apagar led")
        else:
            self.send_response(403)
            self.send_header('Content-type','application/json')
            self.end_headers()
        
        return

class http_server:
    def __init__(self):
        server = HTTPServer(('localhost', 4443), myHandler)
        server.serve_forever()

class main:
    def __init__(self): 
        self.server = http_server()
 
if __name__ == '__main__':
    m = main()