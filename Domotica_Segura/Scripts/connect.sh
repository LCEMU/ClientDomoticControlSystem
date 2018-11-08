#!/bin/bash

sleep 60
if ! ["$(ping -c 1 google.es)"]; then
	python ../Connect_Checker.py;
fi

