# File: Lab2Part1py
# Group: abcd 
# Date: 2/7/2018

# Group Members:
# Sam Beaulieu srb2208
# Doug Soto djs2240
# Alicia Musa am4036

from firebase import firebase
import json as simplejson
import mraa
import time
import pyupm_i2clcd as lcd
from math import log
button_pin = 4
button = mraa.Gpio(button_pin)
button.dir(mraa.DIR_IN)
tempSensor = mraa.Aio(1)
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)

firebase = firebase.FirebaseApplication('https://lab2-f2457.firebaseio.com',None)
result = firebase.get('',None)
print result


B = 4275.0
R0 = 100000.0

def postTemp():
    analog = tempSensor.read()
    R = 1023.0/analog - 1.0
    R *= R0
    temp = 1.0 / (log(R / R0)/B + 1.0/298.15) - 273.15
    tempStr = str(temp) + ' deg C'
    myLcd.setCursor(0,0)
    myLcd.setColor(0,150,150)
    myLcd.write('temp is ' + tempStr+ ' degC')
    
    post = firebase.post('',tempStr)
    print post


try:
    while(1):
        if button.read() == 1:
            postTemp()

except KeyboardInterrupt:
    exit
