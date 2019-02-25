# File: Lab2Part4.py
# Group: abcd 
# Date: 2/13/2018

# Group Members:
# Alicia Musa - am4036@columbie.edu
# Doug Soto - djs2240@columbia.edu
# Sam Beaulieu - srb2208@columbia.edu

import pexpect
import sysrfkill unblock bluetooth
killall bluetoothd
hciconfig hci0 up
from time import sleep


# Code from here used as an example:
# https://github.com/msaunby/ble-sensor-pi/blob/master/sensortag/sensortag_test.py

# Prepare LCD
import pyupm_i2clcd as lcd
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)


# Start pulling temperature through gatttool
uuid = sys.argv[1]
sensor = pexpect.spawn('gatttool -b ' + uuid + ' --interactive')
sensor.expect('\[LE\]>')
print "Connecting. You may need to press the button."
sensor.sendline('connect')
sensor.expect('Connection successful')
print "Connected. Sending notiification request."
sensor.sendline('char-write-req 0x2b 0x01')
sensor.expect('\[LE\]>')
print "Printing data to LCD."

try:
    while True:
        sleep(1)

        # Get temperature from the device
        sensor.expect('Notification handle = 0x002a value: 34 ')
        data = sensor.readline(size=-1).split()
        hex_temp = data[5] + data[4]
        temp = int(hex_temp, 16)/10.0

        # Print the temperature to the LCD
        myLcd.setColor(53, 39, 249)
        myLcd.setCursor(0, 0)
        myLcd.write('Temperature is ')
        myLcd.setCursor(1, 5)
        myLcd.write(str(temp) + ' C') 

except KeyboardInterrupt:
	exit
