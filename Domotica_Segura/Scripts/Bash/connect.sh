#!/bin/bash

sleep 60
if ! ["$(ping -c 1 google.es)"]; then
	python /home/pi/Desktop/Domotica_Segura/Connect_Checker.py;
fi

