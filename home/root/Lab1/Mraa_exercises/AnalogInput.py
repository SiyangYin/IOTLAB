#!/usr/bin/env python
import mraa
from time import sleep
from math import log

B = 4275.0
R0 = 100000.0

def analog_to_celcius(value):
	R = 1023.0/value - 1.0
	R *= R0

	temp = 1.0 / (log(R / R0)/B + 1.0/298.15) - 273.15

	return temp
 
try:
    while(1):
        sleep(0.5)
	tempSensor = mraa.Aio(1)
	temp = analog_to_celcius(tempSensor.read())
	print (temp), "is the current temperature"
except KeyboardInterrupt:
	exit
