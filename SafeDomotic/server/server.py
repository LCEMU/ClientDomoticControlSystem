from http.server import BaseHTTPRequestHandler, HTTPServer
import simplejson as json
import subprocess
import RPi.GPIO as GPIO
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
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(int(pin), GPIO.OUT)
        print("CONFIG")

    ##########################################################################
    # Activamos el GPIO que indica 'pin' al cual esta conectado el actuador
    # Param:
    #   pin, GPIO al cual esta conectado el actuador
    ##########################################################################
    def activate_actuator(self, pin):
        self.config_RPi(int(pin))
        GPIO.output(int(pin), GPIO.HIGH)
        print("ACTIVATE")

    ##########################################################################
    # Desactivamos el GPIO que indica 'pin' al cual esta conectado el actuador
    # Param:
    #   pin, GPIO al cual esta conectado el actuador
    ##########################################################################
    def desactivate_actuator(self, pin):
        self.config_RPi(int(pin))
        GPIO.output(int(pin), GPIO.LOW)
        print("DESACTIVATE")

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
        dev_type = ''

        print(">>> Recibo POST <<<")
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
        print(json_in["Action"] == "On")

        conn = sqlite3.connect('./BBDD/devices_domotica.db')
        cursor = conn.cursor()

        query = "SELECT pin, type FROM device WHERE id=?"
        cursor.execute(query, (id_device,))

        row = cursor.fetchone()

        if row is None:
            print ("No existen dispositivos registrados para este identificador ("+id_device+")")
            self.send_response(400)
            self.send_header('Content-type','application/json')
            self.end_headers()
        else:
            pin = row[0]
            print ("PIN: ", pin)
            dev_type = row[1]
            print ("TIPO: ", dev_type)

            conn.commit()
            conn.close()

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
            self.send_response(400)
            self.send_header('Content-type','application/json')
            self.end_headers()

        return

class http_server:
    def __init__(self):
        wlan0 = subprocess.check_output('ifconfig wlan0 | grep "inet "', shell=True)
        wlan0 = wlan0.split()
        wlan0_map = map(lambda x: x.decode('UTF-8'), wlan0)
        count=0
        if "inet" in wlan0_map:
            ip = wlan0[1].decode('UTF-8')
        else:
            print("ERR")

        server = HTTPServer((ip, 4443), myHandler)
        server.serve_forever()

class main:
    def __init__(self):
        self.server = http_server()

if __name__ == '__main__':
    m = main()
