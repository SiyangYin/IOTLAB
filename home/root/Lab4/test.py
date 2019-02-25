#creates topic, adds subscribers, sends temperature

import boto3
import mraa
from time import sleep

from math import log

button_pin = 4
button = mraa.Gpio(button_pin)
button.dir(mraa.DIR_IN)
tempSensor = mraa.Aio(1)

B = 4275.0
R0 = 100000.0

def analog_to_celcius(value):
	R = 1023.0/value - 1.0
	R *= R0

	temp = 1.0 / (log(R / R0)/B + 1.0/298.15) - 273.15

	return temp


some_list_of_contacts = ["+16464695496"]
#some_list_of_contacts = ["+12105772737", "+16464695496", "+12074000098"]

client = boto3.client(
    "sns",
    aws_access_key_id="AKIAISPM4WGKFE44LZWA",
    aws_secret_access_key="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",
    region_name="us-east-1"    
)

topic = client.create_topic(Name="temp")
topic_arn = topic['TopicArn']

for number in some_list_of_contacts:
    client.subscribe(
        TopicArn=topic_arn,
        Protocol='sms',
        Endpoint=number
    )

print "..."

try:
    while(1):
        if button.read() == 1:
	    temp = analog_to_celcius(tempSensor.read())
            client.publish(Message="Temperature: " + str(temp), TopicArn=topic_arn)
            sleep(0.5)

except KeyboardInterrupt:
	exit
