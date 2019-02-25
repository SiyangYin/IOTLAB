# File: edisonKinesisDemo.py
# Group: abcd 
# Date: 2/7/2018

# Group Members:
# Alicia Musa - am4036@columbie.edu
# Doug Soto - djs2240@columbia.edu
# Sam Beaulieu - srb2208@columbia.edu



########################################################################
# * Assignment 2 Part 3. File written by Peter Wei pw2428@columbia.edu #
########################################################################

import boto
import boto.dynamodb2
import mraa
import time
import json


DYNAMO_TABLE_NAME = 'edisonLab2Part3'
KINESIS_STREAM_NAME = 'edisonLab2Part3'

ACCOUNT_ID = '910224002184'
IDENTITY_POOL_ID = 'us-east-1:0056b741-a8e6-4e34-91dc-993ddf5389b1'
ROLE_ARN = 'arn:aws:iam::910224002184:role/Cognito_edisonDemoKinesisUnauth_Role'


#################################################
# Instantiate cognito and obtain security token #
#################################################
# Use cognito to get an identity.
cognito = boto.connect_cognito_identity()
cognito_id = cognito.get_id(ACCOUNT_ID, IDENTITY_POOL_ID)
oidc = cognito.get_open_id_token(cognito_id['IdentityId'])

# Further setup your STS using the code below
sts = boto.connect_sts()
assumedRoleObject = sts.assume_role_with_web_identity(ROLE_ARN, "XX", oidc['Token'])

# Connect to dynamoDB and kinesis
client_dynamo = boto.dynamodb2.connect_to_region(
	'us-east-1',
	aws_access_key_id=assumedRoleObject.credentials.access_key,
    aws_secret_access_key=assumedRoleObject.credentials.secret_key,
    security_token=assumedRoleObject.credentials.session_token)

client_kinesis = boto.connect_kinesis(
	aws_access_key_id=assumedRoleObject.credentials.access_key,
	aws_secret_access_key=assumedRoleObject.credentials.secret_key,
	security_token=assumedRoleObject.credentials.session_token)

from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey

######################
# Setup DynamoDB Table
######################

table_dynamo = Table(DYNAMO_TABLE_NAME, connection=client_dynamo)

#################################################
# Setup switch and temperature sensor #
#################################################

switch_pin_number = 4
switch = mraa.Gpio(switch_pin_number)
switch.dir(mraa.DIR_IN)

import pyupm_i2clcd as lcd
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)

from time import sleep
from math import log
import datetime

tempSensor = mraa.Aio(1)

B = 4275.0
R0 = 100000.0

def getTemp():
    analog = tempSensor.read()
    R = 1023.0/analog - 1.0
    R *= R0
    temp = 1.0 / (log(R / R0)/B + 1.0/298.15) - 273.15
    return temp


######################
# YOUR CODE HERE #
######################

mode = 'DynamoDB'
myLcd.setColor(53, 30, 249)
myLcd.setCursor(0, 0)
myLcd.write('Writing to ')
myLcd.setCursor(1, 4)
myLcd.write(mode)

try:
	while (1):
            if (switch.read()):
		#######################################
		# When button pressed:
		# Post into DynamoDB
		# Change LCD Display
		#######################################
		######################
		# YOUR CODE HERE #
		######################
                if mode == 'DynamoDB':
                    myLcd.clear()
                    myLcd.setColor(127, 255, 0)
                    mode = 'Kinesis'

		#######################################
		# When button pressed again:
		# Post into Kinesis Stream
		# Change LCD Display
		#######################################
		######################
		# YOUR CODE HERE #
		######################
                elif mode == 'Kinesis':
                    myLcd.clear()
                    myLcd.setColor(53, 39, 249)
                    mode = 'DynamoDB'

            if mode == 'DynamoDB':
                table_dynamo.put_item(data = {
                    'timestamp': str(datetime.datetime.now()), 
                    'temperature': str(getTemp())
                })
            elif mode == 'Kinesis':
                payload = '{\'timestamp\': \'' + str(datetime.datetime.now()) + '\',\'temperature\': \'' + str(getTemp()) + '\'}'
                client_kinesis.put_record(
                    KINESIS_STREAM_NAME,
                    payload.encode(),
                    'Shard1'
                )


            myLcd.setCursor(0, 0)
            myLcd.write('Writing to ')
            myLcd.setCursor(1, 4)
            myLcd.write(mode)

            sleep(0.1)

except KeyboardInterrupt:
	exit
