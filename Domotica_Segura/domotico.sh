#!/bin/bash

#python BBDD/CrearBBDD.py
python3 server/server.py &
python conectarDispositivos.py
