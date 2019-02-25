#**********************************************************************************************
# * Copyright (C) 2015-2016 Sareena Abdul Razak sta2378@columbia.edu
# * 
# * This file is part of New-York-MTA-Subway-Trip-Planner.
# * 
# * New-York-MTA-Subway-Trip-Planner can not be copied and/or distributed without the express
# * permission of Sareena Abdul Razak
# *********************************************************************************************

# Contains all functions needed to get a aws client or resource
# Used in ../dataAnalysis/S3.py and ../dataAnalysis/createAMLModel.py

import boto3
from boto3.dynamodb.conditions import Key, Attr
from time import sleep, time
	
COGNITO_ID = "EdisonApp"
ACCOUNT_ID = "910224002184"
IDENTITY_POOL_ID = "us-east-1:c0564c8b-7686-4770-9513-2c55901823d1"
ROLE_ARN = "arn:aws:sns:us-east-1:910224002184:Demo_Topic" 
REGION = "us-east-1"

def getCredentials():
	# Use cognito to get an identity from AWS for the application residing on Edison
	# boto3.client function helps you get a client object of any AWS service
	# Here for example we are getting a client object of AWS cognito service
	cognito = boto3.client('cognito-identity', REGION) 
	cognito_id = cognito.get_id(AccountId=ACCOUNT_ID, IdentityPoolId=IDENTITY_POOL_ID)
	oidc = cognito.get_open_id_token(IdentityId=cognito_id['IdentityId'])

	    # Similar to the above code, here we are getting a client object for AWS STS service
	sts = boto3.client('sts')
	assumedRoleObject = sts.assume_role_with_web_identity(RoleArn=ROLE_ARN,\
	                     RoleSessionName=COGNITO_ID,\
	                    WebIdentityToken=oidc['Token'])

	    # This contains Access key Id and secret access key and sessiontoken to connect to dynamodb
	credentials = assumedRoleObject['Credentials']
	return credentials


def getResource(resourceName):
	credentials = getCredentials()
	resource = boto3.resource(resourceName,
			 REGION,
	        aws_access_key_id= credentials['AccessKeyId'],
	        aws_secret_access_key=credentials['SecretAccessKey'],
	        aws_session_token=credentials['SessionToken'])
	return resource

def getClient(clientName):
	credentials = getCredentials()
	client = boto3.client(clientName,
			 REGION,
	        aws_access_key_id= credentials['AccessKeyId'],
	        aws_secret_access_key=credentials['SecretAccessKey'],
	        aws_session_token=credentials['SessionToken'])
	return client

def deleteOldItems(table = None):

        dynamo = getResource('dynamodb')

        # Get the dynamo table if need be
        if table == None:
            table = getDynamoTable("mtaUpdates")

        # Scan the table for old timestamps
        current_time = int(time())
        items = table.scan(FilterExpression=Attr('timeStamp').lt(current_time - 2 * 60))    

        # Delete each of the entries that are recieved
        num = 0
        with table.batch_writer() as batch:
            for each in items['Items']:
                batch.delete_item(
                    Key = {
                        'tripId': str(each['tripId']),
                        'timeStamp': int(each['timeStamp'])
                    }
                )
                num += 1

        print 'Deleted ' + str(num) + ' items from the table ' + table.name + '.'
        
        

 

def getDynamoTable(tableName):
    
        dynamo = getResource('dynamodb')

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



