#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('/home/pi/Desktop/Domotica_Segura/BBDD/devices_domotica.db')

cursor = conn.cursor()

print("La base de datos se abrio correctamente")

cursor.execute('''CREATE TABLE data_device
                (ID INT PRYMARY KEY NOT NULL,
                NOMBRE TEXT NOT NULL,
                TIPO CHAR(1) NOT NULL,
                FECHA TEXT NOT NULL,
                HORA TEXT NOT NULL,
                DATO TEXT NOT NULL)''')

print ("La tabla ha sido creada con exito")

conn.close()