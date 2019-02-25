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

import boto3
from boto3.dynamodb.conditions import Key,Attr

sys.path.append('../utils')
import tripupdate,vehicle,alert,mtaUpdates,aws

### YOUR CODE HERE ####
DYNAMO_TABLE_NAME = 'mtadata'
#update = mtaUpdates

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
                        }                    ],
                    AttributeDefinitions = [
                        {
                            'AttributeName': 'tripId',
                            'AttributeType': 'S'
                        }                    ],
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

class dynamoMethods:
    def __init__(self, dbName):
        self.table_dynamo = getDynamoTable(DYNAMO_TABLE_NAME)

    def dynamoAdd(self, trip_Id, routeId, startDate, direction, currentStopId, currentStopStatus, vehicleTimeStamp, futureStopData, timeStamp):

        try:
            mtadata = self.table_dynamo.get_item(Key = {
                'tripId' : trip_Id
            })
            #mtadata['tripId'] = tripId
            mtadata['routeId'] = routeId
            mtadata['startDate'] = startDate
            mtadata['direction'] = direction
            mtadata['currentStopId'] = currentStopId
            mtadata['currentStopStatus'] = currentStopStatus
            mtadata['vehicleTimeStamp'] = vehicleTimeStamp
            mtadata['futureStopData'] = futureStopData
            mtadata['timeStamp'] = timeStamp
            mtadata.save(overwrite=True)
            #print "Entry updated.\n"

        except Exception as e:
            #print str(e) + '\n'
            self.table_dynamo.put_item(Item={
                'tripId' : trip_Id,
                'routeId' : routeId,
                'startDate' : startDate,
                'direction' : direction,
                'currentStopId' : currentStopId,
                'currentStopStatus' : currentStopStatus,
                'vehicleTimeStamp' : vehicleTimeStamp,
                'futureStopData' : futureStopData,
                'timeStamp' : timeStamp,
            })
            #print "New entry created.\n"
    
    def dynamoDelete(self):

        # Scan the table for old timestamps
        current_time = int(time.time())
        items = self.table_dynamo.scan(FilterExpression=Attr('timeStamp').lt(current_time - 2 * 60))    

        # Delete each of the entries that are recieved
        num = 0
        with self.table_dynamo.batch_writer() as batch:
            for each in items['Items']:
                batch.delete_item(
                    Key = {
                        'tripId': str(each['tripId'])
                    }
                )
                num += 1
    
        print 'Deleted ' + str(num) + ' items from before ' + str(current_time - 120) + ' from table ' + self.table_dynamo.name + '.'


    def dynamoViewAll(self):
        pass

mta = mtaUpdates.mtaUpdates()
DB = dynamoMethods(DYNAMO_TABLE_NAME)
def firstTask():
    try:
        while(1):
            #add data to table
            timeStamp, updates = mta.getTripUpdates()
            
            num = 0
            for item in updates:
                #fill these variables
                tripId = item.tripId
                routeId = item.routeId if item.routeId != '' else ' '
                startDate = item.startDate
                direction = item.direction
                if item.vehicleData:
                    currentStopId = item.vehicleData.currentStopId
                    currentStopStatus = item.vehicleData.currentStopStatus
                    vehicleTimeStamp = item.vehicleData.timestamp
                else:
                    currentStopId = ' '
                    currentStopStatus = ' '
                    vehicleTimeStamp = ' '
                futureStopData = item.futureStops

                DB.dynamoAdd(tripId, routeId, startDate, direction, currentStopId, currentStopStatus, vehicleTimeStamp, futureStopData, timeStamp)
                num += 1

            print 'Added ' + str(num) + ' items at time ' + str(timeStamp) +' to table ' + DB.table_dynamo.name + '.'

            time.sleep(30)


    except KeyboardInterrupt:
        exit

def secondTask():
    try:
        while(1):
            #delete data that is older than 2min
            DB.dynamoDelete()

            time.sleep(60)



    except KeyboardInterrupt:
        exit

t1 = Thread(target=firstTask)
t2 = Thread(target=secondTask)
t1.start()
t2.start()
