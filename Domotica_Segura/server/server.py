from http.server import BaseHTTPRequestHandler, HTTPServer
import simplejson
import RPi.GPIO as GPIO
import numpy as np

class myHandler(BaseHTTPRequestHandler):

    def config_rele(self, pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)

    def activa_rele(self, pin):
        self.config_rele()
        GPIO.output(pin, GPIO.HIGH)

    def desactiva_rele(self, pin):
        self.config_rele()
        GPIO.output(pin, GPIO.LOW)

    def do_POST(self):
            print(">>> Recibo POST <<<")
            print("[[ CONTENT-LENGTH ]]: ",int(self.headers['Content-Length']))
            post_body = self.rfile.read(int(self.headers['Content-Length']))
            print("[[ BODY ]]\n",post_body)

            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            json_in = simplejson.loads(post_body)

            print("{}".format(json_in))
            id = json_in["Id"]
            action = json_in["Action"]
            print("ID: ",id)
            print("ACTION: ",action)
            print(json_in["Action"] == "On")

            #leer fichero perifericos.dat y seleccionar la linea que guarde el dispositico con el id data[Id]
            # cogemos el pin asignado a este actuador y realizamos la accion que nos indique data[Action]
            f = open("../perifericos.txt", "r")
            dt = np.dtype('|U25')
            data = np.loadtxt(f, dt, delimiter=" ", skiprows=1)
            f.close()
            print("DATA\n", data)
            dat = data[data[:,0]==id]
            print("SELECT: ", dat.decode())

            if json_in["Action"] == "On":
                #Encender led
                self.activa_rele(pin)
                print("Encender led")
            else:
                #Apagar led
                self.desactiva_rele(pin)
                print("Apagar led")

            return

class http_server:
    def __init__(self):
        server = HTTPServer(('localhost', 8080), myHandler)
        server.serve_forever()

class main:
    def __init__(self): 
        self.server = http_server()
 
if __name__ == '__main__':
    m = main()
