import os
from urllib import request
import json
from json import loads
import requests
from requests import get
import datetime
from dotenv import load_dotenv
import pandas as pd

load_dotenv() 

api = os.environ.get('api')
api2 = os.environ.get('api2')


"""
Retrive random quotes from api forismatic
"""

def get_quotes():
    try: #retrieve quotes
        response = get('http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en')
        return '{quoteText} - {quoteAuthor}'.format(**loads(response.text))

    except Exception as e:
        print('Life goes on, no matter your struggles - Beauty Ikudehinbu')
"""
Retrieve the current weather forecast from OpenWeatherMap.
"""
def get_weather_forecast(coords={'lat': -1.9441, 'lon': 30.0619}): # default location at Kigali,
    try: # retrieve forecast for specified coordinates
        
        url = f'https://api.openweathermap.org/data/2.5/forecast?lat={coords["lat"]}&lon={coords["lon"]}&appid={api}&units=metric'
        data = json.load(request.urlopen(url))

        forecast = {'city': data['city']['name'], # city name
                    'country': data['city']['country'], # country name
                    'periods': list()} # list to hold forecast data for future periods

        for period in data['list'][0:9]: # populate list with next 9 forecast periods 
            forecast['periods'].append({'timestamp': datetime.datetime.fromtimestamp(period['dt']),
                                        'temp': round(period['main']['temp']),
                                        'description': period['weather'][0]['description'].title()})
                                        # 'icon': f'http://openweathermap.org/img/wn/{period["weather"][0]["icon"]}.png'})
        
        return forecast

    except Exception as e:
        print("\nThere are issues when generating today's weather forecast",e)        


def matches():
    try:
        uri = 'https://api.football-data.org/v4/matches'
        headers = { 'X-Auth-Token': api2 }
        response = (requests.get(uri, headers=headers)).json()

        for match in response['matches']:
            df = pd.DataFrame(match)
            print(df)

    except Exception as e:
        print(" Sorry, We couldn't get today's match", e)


if __name__ == '__main__':
   
    print("------ Quote of the day ------")
    print(get_quotes())

    forecast = get_weather_forecast() # get forecast for default location
    if forecast:
        print(f'\n------ Weather forecast for {forecast["city"]}, {forecast["country"]} ------')
        for period in forecast['periods']:
            print(f' - {period["timestamp"]} | {period["temp"]}°C | {period["description"]}')

    print("\n---Football matches---")
    print(matches())