# Group: abcd
# Group Members:
# Alicia Musa- am4036
# Doug Soto- djs2240
# Sam Beaulieu- srb2208

import urllib2,contextlib
from datetime import datetime
from collections import OrderedDict

from pytz import timezone
from google.transit import gtfs_realtime_pb2
import google.protobuf
import json 

import vehicle,alert,tripupdate

# cf0fa9cc7db7329db1d238069e694c7c

class mtaUpdates(object):

    # Do not change Timezone
    TIMEZONE = timezone('America/New_York')
    
    # feed url depends on the routes to which you want updates
    # here we are using feed 1 , which has lines 1,2,3,4,5,6,S
    # While initializing we can read the API Key and add it to the url
    feedurl = 'http://datamine.mta.info/mta_esi.php?feed_id=1&key='
    
    VCS = {1:"INCOMING_AT", 2:"STOPPED_AT", 3:"IN_TRANSIT_TO"}    
    #tripUpdates = []
    alerts = []

    def __init__(self,apikey = 'cf0fa9cc7db7329db1d238069e694c7c'):
        self.feedurl = self.feedurl + apikey

    # Method to get trip updates from mta real time feed
    def getTripUpdates(self):
        feed = gtfs_realtime_pb2.FeedMessage()
        try:
            with contextlib.closing(urllib2.urlopen(self.feedurl)) as response:
                d = feed.ParseFromString(response.read())
        except (urllib2.URLError, google.protobuf.message.DecodeError) as e:
            print "Error while connecting to mta server " + str(e)
	

	timestamp = feed.header.timestamp
        nytime = datetime.fromtimestamp(timestamp,self.TIMEZONE)
        #print nytime
        #print timestamp

        tripUpdates = []
        updateIndices = {}

        for entity in feed.entity:
	    # Trip update represents a change in timetable
	    if entity.trip_update and entity.trip_update.trip.trip_id:
		update = tripupdate.tripupdate()
                update.tripId = entity.trip_update.trip.trip_id
                update.routeId = entity.trip_update.trip.route_id
                update.startDate = entity.trip_update.trip.start_date
                update.direction = entity.trip_update.trip.trip_id[-4]
                '''
                if entity.vehicle:
                    update.vehicleData = entity.vehicle
                '''
                for item in entity.trip_update.stop_time_update:
                    arrivalTime = item.arrival.time 
                    departureTime = item.departure.time 
                    update.futureStops[item.stop_id] = {
                            'arrivalTime': arrivalTime,
                            'departureTime': departureTime
                    }
                updateIndices[entity.trip_update.trip.trip_id] = len(tripUpdates)
                tripUpdates.append(update)
                
                '''
                trip_update {
                  trip {
                      trip_id: "060100_1..N03R"
                      start_date: "20180214"
                      route_id: "1"
                   }
                   stop_time_update {
                      arrival {
                          time: 1518624541
                       }
                       departure {
                          time: 1518624841
                       }
                       stop_id: "103N"
                    }
                    stop_time_update {
                        arrival {
                           time: 1518624931
                        }
                        stop_id: "101N"
                    }
                }
                '''

	    if entity.vehicle and entity.vehicle.trip.trip_id:
	    	v = vehicle.vehicle()
                v.currentStopNumber = entity.vehicle.current_stop_sequence
                v.currentStopId = entity.vehicle.stop_id
                v.timestamp = entity.vehicle.timestamp
                v.currentStopStatus = entity.vehicle.current_status

                # Search trip updates for trip
                if entity.vehicle.trip.trip_id in updateIndices:
                    tripUpdates[updateIndices[entity.vehicle.trip.trip_id]].vehicleData = v
                else:
                    print 'not found'

                '''            
                found = False
                for trips in self.tripUpdates:
                    if trips.tripId == entity.vehicle.trip.trip_id:
                        trips.vehicleData = v
                        found = True
                        break
                if not found:
                    print 'not found'
                '''
                #self.tripUpdates.append(v)

                '''
                vehicle {
                  trip {
                      trip_id: "063200_6..N03R"
                      start_date: "20180214"
                      route_id: "6"
                   }
                   current_stop_sequence: 26
                   current_status: INCOMING_AT
                   timestamp: 1518624792
                   stop_id: "614N"
                }
                '''
            
	    if str(entity.alert).strip():
                a = alert.alert()
                
                for item in entity.alert.header_text.translation:
                    a.alertMessage = item.text
                
                for item in  entity.alert.informed_entity:                  
                    a.tripId.append(item.trip.trip_id)
                    a.routeId[item.trip.trip_id] = item.trip.route_id
                
	        if entity.trip_update and entity.trip_update.trip.trip_id:
                    a.startDate[entity.trip_update.trip.trip.trip_id] = entity.trip_update.trip.start_date
                
                self.alerts.append(a)

                
                '''
                alert {
                    informed_entity {
                        trip {
                            trip_id: "066850_1..N03R"
                            route_id: "1"
                        }
                    }
                    header_text {
                        translation {
                            text: "Train delayed"
                        }
                    }
                }
                '''
        
	return timestamp, tripUpdates
    
    # END OF getTripUpdates method
