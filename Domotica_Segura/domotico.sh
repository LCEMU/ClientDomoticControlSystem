#!/bin/bash

rm ./BBDD/devices_domotica.db
python BBDD/CrearBBDD.py
python3 server/server.py &
python conectarDispositivos.py
