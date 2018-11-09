#!/bin/bash

rm ./BBDD/DomoticControlSystem.db
python ./BBDD/CrearBBDD.py
python3 ./server/server.py &
python ./conectarDispositivos.py
