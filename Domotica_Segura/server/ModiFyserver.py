from http.server import BaseHTTPRequestHandler, HTTPServer
import simplejson
#import RPi.GPIO as GPIO
import json
import numpy as np

class myHandler(BaseHTTPRequestHandler):
        
    def config_RPi(self, pin):
        '''
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        '''
        return "------> Ini actuador"

    def activate_actuator(self, pin):
        '''
        self.config_RPi()
        GPIO.output(pin, GPIO.HIGH)
        '''
        return "------> Activar actuador"
        
    def desactivate_actuator(self, pin):
        '''
        self.config_RPi()
        GPIO.output(pin, GPIO.LOW)
        '''
        return "------> Desactivar actuador"

    def do_GET(self):
        print(">>> Recibido GET <<<")

    def do_POST(self):
        print(">>> Recibo POST <<<")

        print("[[ A - CONTENT-LENGTH ]]: ",self.headers.get('content-length'))
        length = int(self.headers.get('content-length'))
        #field_data = self.rfile.read(length)
        #fields = urlparse.parse_qs(field_data)


        #print("[[ CONTENT-LENGTH ]]: ",self.headers['Content-type'])
        #post_body = str(self.rfile.read(self.headers['Content-type']))
        post_body = str(self.rfile.read(length))
        print("[[ BODY ]]\n",post_body)
        print("[[ TYPE-BODY ]]\n",type(post_body))

        chars = ['\\n','\\','`','*','_','{','}','[',']','(',')','>','#','+','-','.','!','$','\'','b']
        for c in chars:
            post_body = post_body.replace(c,"")
        '''
        json_in_a = post_body.replace("\\n", "")
        print ("JSON A: ",json_in_a)
        json_in_b = json_in_a.replace("\\", "")
        print ("JSON B: ",json_in_b)
        json_in_c = json_in_b.replace("b", "")
        print ("JSON C: ",json_in_c)
        json_in_d = json_in_c.replace("'", "")
        print ("JSON D: ",json_in_d)
        json_in_e = json_in_d.replace("{", "")
        print ("JSON E: ",json_in_e)
        json_in_f = json_in_e.replace("}", "")
        print ("JSON F: ",json_in_f)
        
        id = post_body["Id"]
        action = post_body["Action"]
        print("ID: ",id)
        print("ACTION: ",action)        
        '''
        print ("POST BOSY CLEAN: ", post_body)
        if "Id" in post_body and "Action" in post_body:
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()

            post_body.index("Id")

        json_in = post_body.split(",")
        json_id = json_in[0]
        json_action = json_in[1]
        print ("SPLIT: ",json_in)

        print("JSON_IN: ", json_in[0])

        '''
        json_in = json.decoder(post_body)
        print ("JSON: ")
        print(json_in)
        
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
            self.activate_actuator(pin)
            print("Encender led")
        else:
            #Apagar led
            self.desactivate_actuator(pin)
            print("Apagar led")
        '''
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