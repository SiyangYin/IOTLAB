import json
import requests

weatherKey = '55fc80b6a15247b8ec899ea0ed0119cc'
nycLat = 40.7128
nycLng = -74.006
bosLat = 42.3601
bosLng = -71.0589
satLat = 29.4241
satLng = -98.4936
chiLat = 41.8781
chiLng = -87.6298
req = "{'content type' : 'applications/jsonrequests', 'content length' : '0'}"

print 'weather in san antonio'
weather = "http://api.openweathermap.org/data/2.5/weather?lat=" + str(satLat) + "&lon=" + str(satLng) + "&appid=" + weatherKey

#weather = "http://api.openweathermap.org/data/2.5/weather?SanAntonio" + "&appid=" + weatherKey

r1 = requests.get(weather, data =req)
res1 = json.loads(r1.text)

temp = res1["main"]["temp"]
desc = res1["weather"][0]["description"]
tempc = temp-273.15
print str(tempc) + " deg C" 
print str(desc)
