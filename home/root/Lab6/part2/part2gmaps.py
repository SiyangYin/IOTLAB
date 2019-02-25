def route(lat1,lng1,lat2,lng2):

    import googlemaps
    from datetime import datetime
    import json


    gmaps = googlemaps.Client(key="AIzaSyD04cLoGwkT-HA9i2IPLotf7hnT1AuM03Y")
    now = datetime.now()
    steps = []

    source = (lat1, lng1)
    destination = (lat2,lng2)

    directions = gmaps.directions(source,destination,mode="driving",departure_time=now)

    for leg in directions[0]['legs']:
        for step in leg['steps']:
            steps.append(step['html_instructions'])
    return steps



