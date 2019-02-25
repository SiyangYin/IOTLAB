# lab1
# group ABCD
# 02/09/19
# Siyang Yin sy2820
# Ruilong Tang rt2701
# Zirui Tan zt2219

import mraa
import time
import pyupm_i2clcd as lcd
from math import log
button_pin = 4
button = mraa.Gpio(button_pin)
button.dir(mraa.DIR_IN)
tempSensor = mraa.Aio(1)
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)

B = 4275.0
R0 = 100000.0

def displayTemp():
    analog = tempSensor.read()
    R = 1023.0/analog - 1.0
    R *= R0
    temp = 1.0 / (log(R / R0)/B + 1.0/298.15) - 273.15
    tempStr = str(temp)
    myLcd.setCursor(0,0)
    myLcd.setColor(255,0,0)
    myLcd.write('temp is ' + tempStr+ 'degC')

while(1):
    if button.read() == 1:
        displayTemp()

/Users/siyangyin/Desktop/未命名文件夹
