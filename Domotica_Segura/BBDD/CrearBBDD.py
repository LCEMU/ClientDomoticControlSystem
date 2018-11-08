#!/usr/bin/python

import sqlite3

print("\nIntentamos crear la BBDD...")
conn = sqlite3.connect('./BBDD/devices_domotica.db')

cursor = conn.cursor()

print(">> [OK] << La base de datos se abrio correctamente")

print("\nIntentamos crear la tabla DEVICE...")
cursor.execute('''CREATE TABLE device
                (ID INT PRIMARY KEY NOT NULL,
                PIN TEXT NOT NULL,
                NAME TEXT NOT NULL,
                TYPE CHAR(1) NOT NULL)''')
print (">> [OK] << La tabla DEVICE ha sido creada con exito")


print("\nIntentamos crear la tabla ACTIVITY_DEVICE...")
cursor.execute('''CREATE TABLE activity_device
                (ID INT NOT NULL,
                DDATE TEXT NOT NULL,
                TIME TEXT NOT NULL,
                INFO TEXT NOT NULL)''')
print (">> [OK] << La tabla ACTIVITY_DEVICE ha sido creada con exito")

#print("\nIntentamos crear PK para DEVICE(id, pin)...")
#cursor.execute('''ALTER TABLE device ADD CONSTRAINT pk_device PRYMARY KEY (ID, PIN)''')
#print (">> [OK] << La PK para DEVICE(id, pin) ha sido creada con exito")

#print("\nIntentamos crear una PK para ACTIVITY_DEVICE(id, fecha, hora)...")
#cursor.execute('''ALTER TABLE activity_device ADD PRYMARY KEY (id, fecha, hora)''')
#print (">> [OK] << La PK para ACTIVITY_DEVICE(id, fecha, hora) ha sido creada con exito")

#print("\nIntentamos crear una FK para ACTIVITY_DEVICE(id)...")
#cursor.execute('''ALTER TABLE activity_device ADD CONSTRAINT fk_device_activityDevice
#					FOREIGN KEY (id)
#					REFERENCES device(id)''')
#print (">> [OK] << La PK para FK para ACTIVITY_DEVICE(id) ha sido creada con exito")

conn.close()

'''

.headers ON
.mode columns

SELECT * FROM device;
SELECT * FROM activity_device;

INSERT INTO device(id, pin, name, type) values (1, 17, 'Rele', 'A');
INSERT INTO device(id, pin, name, type) values (2, 23, 'TempHum', 'S');

INSERT INTO activity_device(id, ddate, time, info) values (1, '08/11/2018', '14:04:49', 'Disable');
INSERT INTO activity_device(id, ddate, time, info) values (1, '08/11/2018', '14:06:01', 'Enable');
INSERT INTO activity_device(id, ddate, time, info) values (1, '08/11/2018', '14:08:50', 'Disable');
INSERT INTO activity_device(id, ddate, time, info) values (1, '08/11/2018', '14:10:20', 'Disable');

INSERT INTO activity_device(id, ddate, time, info) values (2, '08/11/2018', '14:04:49', 'T: " + 15 oC + " - H:20');
INSERT INTO activity_device(id, ddate, time, info) values (2, '08/11/2018', '14:06:01', 'T: " + 18 oC + " - H:33');
INSERT INTO activity_device(id, ddate, time, info) values (2, '08/11/2018', '14:08:50', 'T: " + 14 oC + " - H:12');
INSERT INTO activity_device(id, ddate, time, info) values (2, '08/11/2018', '14:10:20', 'T: " + 20 oC + " - H:60');
'''
