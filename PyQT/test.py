import sys
import requests
import json 
 
city_id = ''
city = "Rivne"
cities = requests.get('http://bulk.openweathermap.org/sample/weather_16.json.gz')

data = json.load(f)
for item in data:
    if item['city']['name'] == city:
        print(item['city']['id'])
