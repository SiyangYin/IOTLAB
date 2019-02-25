# Group: abcd
# Group Members:
# Alicia Musa- am4036
# Doug Soto- djs2240
# Sam Beaulieu- srb2208
# *********************************************************************************************
# Program to update dynamodb with latest data from mta feed. It also cleans up stale entried from db
# Usage python dynamodata.py
# *********************************************************************************************
import json,time,sys
from collections import OrderedDict
from threading import Thread
import csv
import boto3
from boto3.dynamodb.conditions import Key,Attr
import sys

sys.path.append('../utils')
import tripupdate,vehicle,alert,mtaUpdates,aws


DYNAMO_TABLE_NAME = 'mtadata'
client = boto3.client(
    "sns",
    aws_access_key_id="AKIAIGF773AWXFY3JKKA",
    aws_secret_access_key="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",
    region_name="us-east-1"
)
topic = client.create_topic(Name="mtaSubscribers")
topic_arn = topic['TopicArn']

def getDynamoTable(tableName):
    
        dynamo = aws.getResource('dynamodb')

        # First try and create the table
        try:
            table = dynamo.create_table(
                    TableName = tableName,
                    KeySchema = [
                        {
                            'AttributeName': 'tripId',
                            'KeyType': 'HASH' # Partition Key
                        },
                        {
                            'AttributeName': 'timeStamp',
                            'KeyType': 'RANGE' # Sort key
                        }
                    ],
                    AttributeDefinitions = [
                        {
                            'AttributeName': 'tripId',
                            'AttributeType': 'S'
                        },                        
                        {
                            'AttributeName': 'timeStamp',
                            'AttributeType': 'N'
                        }
                    ],
                    ProvisionedThroughput = {
                        'ReadCapacityUnits': 10,
                        'WriteCapacityUnits': 10
                    }
                )
            while table.table_status != 'ACTIVE':
                table.reload()
                sleep(0.2)
            print 'Table ' + tableName + ' has been created.'
        except Exception as e:
            #print e
            table = dynamo.Table(tableName)
            print 'Table ' + tableName + ' has been retrieved.'

        return table



class mtaMethods:
    def __init__(self, dbName):
        self.table_dynamo = getDynamoTable(DYNAMO_TABLE_NAME)
        
        # Load stops data
        self.stops = {}
        with open('stops.csv') as stops:
            reader = csv.reader(stops)
            for each_stop in reader:
                try:
                    stopId = int(each_stop[0])
                except:
                    stopId = 128
                if each_stop[2] not in self.stops and each_stop[0][0] == '1' and stopId < 121:
                    self.stops[each_stop[2].strip()] = each_stop[0]
                    #print each_stop[2]


    def getTrains(self, direction):
        local = self.table_dynamo.scan(FilterExpression=Attr('routeId').eq('1') & Attr('vehicalTimeStamp').ne(' ') & Attr('direction').eq(direction))
        express = self.table_dynamo.scan(FilterExpression=(Attr('routeId').eq('2') | Attr('routeId').eq('3')) & Attr('vehicalTimeStamp').ne(' ') & Attr('direction').eq(direction))

        return local, express

    def printValidStops(self):
        print '\nValid stops are: '
        for stops in self.stops:
            print '- ' + stops
        print ''

    def planTrip(self, direction, station):

        # Get station id
        if station in self.stops:
            stationId = self.stops[station]
        else:
            self.printValidStops()
            return

        print ''
        
        # Get local and express data and print trip ids
        local_temp, express_temp = self.getTrains(direction)
        fastest = sys.maxint
        transfer = False
        print 'Local Trips:'
        for trip in local_temp['Items']:
            if str(stationId)+direction in trip['futureStopData'] and '120'+direction in trip['futureStopData']:
                print '- ' + trip['tripId']
                if trip['futureStopData']['120'+direction]['arrivalTime'] < fastest:
                    fastest = trip['futureStopData']['120'+direction]['arrivalTime']
                    fastest_trip = trip

        try:
            print 'Earliest local train to 96: ' + fastest_trip['tripId']
        except:
            print 'There are no local trains to 96th street.'

        fastest_ex = sys.maxint
        print '\nExpress Trips:'
        for trip in express_temp['Items']:
            if '120'+direction in trip['futureStopData']:
                print '- ' + trip['tripId']
                if trip['futureStopData']['120'+direction]['arrivalTime'] > fastest:
                    if trip['futureStopData']['120'+direction]['arrivalTime'] < fastest_ex:
                        fastest_ex = trip['futureStopData']['120'+direction]['arrivalTime']
                        fastest_ex_trip = trip
        try:
            print 'Earliest express train to 96: ' + fastest_ex_trip['tripId']
        except:
            print 'There are no express trains to 96th street.'

        print ''
        try:
            fastest_trip
            fastest_ex_trip
        except NameError:
            print 'No valid path found. Good luck!'
            return 

        if direction == 'S':
            try:
                fastest_trip['futureStopData']['127S']
                fastest_ex_trip['futureStopData']['127S']
            except:
                print 'No path to 42nd found.'
                return 

            print 'The local will arrive at 42 at: ' + str(fastest_trip['futureStopData']['127S']['arrivalTime'])
            print 'The express will arrive at 42 at: ' + str(fastest_ex_trip['futureStopData']['127S']['arrivalTime'])
            print ''

            if fastest_trip['futureStopData']['127S']['arrivalTime'] < fastest_ex_trip['futureStopData']['127S']['arrivalTime']:
                message = 'Stay on the Local Train'
            else:
                message = 'Switch to Express Train'
        if direction == 'N':
            if fastest < fastest_ex:
                message = 'Stay on the Local Train'
            else:
                message = 'Switch to Express Train'

        print message
        print ''
        client.publish(Message=message, TopicArn=topic_arn)

        return 0
             
    def subscribeToMessageFeed(self, num):
        try:
            client.subscribe(
                TopicArn=topic_arn,
                Protocol='sms',
                Endpoint=num
            )
        except:
            print '\nAn error occured. Please make sure you entered a number correctly.'
            print '- Number format: +12345678900\n'

        return 0

    
mta = mtaUpdates.mtaUpdates()
methods = mtaMethods(DYNAMO_TABLE_NAME)

state = 0
src_station = 96
dst_station = 42
number = 0

def get_prompt(state_var):
    if state_var == 0:
        return "Choose an option.\n1. Plan a trip\n2. Subscribe to message feed\n3. Exit\n"
    elif state_var == 1:
        return "Enter the direction you would like to go in (N or S): "
    elif state_var == 2:
        return "Enter the destination station (ie. 116, 96, 110): "
    elif state_var == 3:
        return "Enter the source station (ie. 116, 96, 110): "
    elif state_var == 4:
        return "Enter a number to subscibe: "
    else:
        return "Bad command..."

try:
    while True:
        prompt = get_prompt(state)
        ans = raw_input(prompt)

        if state == 0:
            if ans == "1":
                state = 1
            elif ans == "2":
                state = 4
            elif ans == "3":
                state = 5
                sys.exit("Exiting")
            else:
                print "Unsupported command.\n"
        elif state == 1:
            direction = ans
            if ans == "N":
                state = 2
            elif ans == "S":
                state = 3
            else:
                print "Not a valid direction."
                state = 0
        elif state == 2:
            state = 0
            station = ans
            methods.planTrip(direction, station)
        elif state == 3:
            state = 0
            station = ans
            methods.planTrip(direction, station)
        elif state == 4:
            state = 0
            number = ans
            methods.subscribeToMessageFeed(number)
        else:
            state = 0
            print "Something is wrong."

except KeyboardInterrupt:
    exit

