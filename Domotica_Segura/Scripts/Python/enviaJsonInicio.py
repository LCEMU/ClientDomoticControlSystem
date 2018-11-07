#!/usr/bin/python

import sys
import sqlite3

if __name__ == '__main__':
    
    dirFichero = '/var/www/html/Register/logs.txt'
    f = open(dirFichero, 'r')
    
    json = f.readlines()
    print(type(json[0]),json[0])
    
    f.close()
    
    conn = sqlite3.connect('/home/pi/Documents/TFG/Domotica_Segura/devices_domotica.db')

    cursor = conn.cursor()
    
    print("La base de datos se abrio correctamente")
    
    cursor.execute('''CREATE TABLE jsonSend
                (ID INT PRYMARY KEY NOT NULL,
                JSON TEXT NOT NULL)''')
    
    print ("La tabla ha sido creada con exito")
    
    query = "INSERT INTO jsonSend (id, json) VALUES (?,?)"
    cursor.execute(query, (1, json[0]))
    
    print ("Los datos se han insertado con exito")
    
    conn.commit()
    conn.close()