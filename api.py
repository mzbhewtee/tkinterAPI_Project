import csv
from env import api, api2
from urllib import request
import json
from json import loads
import requests
from requests import get
import datetime

uri = 'https://api.football-data.org/v4/matches'
headers = { 'X-Auth-Token': api2 }

response = requests.get(uri, headers=headers)
for match in response.json()['matches']:
  print (match)
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
def get_weather_forecast(coords={'lat': -1.9441, 'lon': 30.0619}): # default location at Cape Canaveral, FL
    try: # retrieve forecast for specified coordinates
        api_key = api # replace with your own OpenWeatherMap API key
        url = f'https://api.openweathermap.org/data/2.5/forecast?lat={coords["lat"]}&lon={coords["lon"]}&appid={api_key}&units=metric'
        data = json.load(request.urlopen(url))

        forecast = {'city': data['city']['name'], # city name
                    'country': data['city']['country'], # country name
                    'periods': list()} # list to hold forecast data for future periods

        for period in data['list'][0:9]: # populate list with next 9 forecast periods 
            forecast['periods'].append({'timestamp': datetime.datetime.fromtimestamp(period['dt']),
                                        'temp': round(period['main']['temp']),
                                        'description': period['weather'][0]['description'].title(),
                                        'icon': f'http://openweathermap.org/img/wn/{period["weather"][0]["icon"]}.png'})
        
        return forecast

    except Exception as e:
        print("Rhere are issues when generating today's weather forecast")        

def get_twitter_trends():
    pass

def get_wikipedia_article():
    pass

if __name__ == '__main__':
    ##### test get_random_quote() #####
    # print('\nTesting quote generation...')
    print("------ Quote of the day ------")
    print(get_quotes())
    # print(f' - Random quote is "{quote["quote"]}" - {quote["author"]}')

    # quote = get_random_quote(quotes_file = None)
    # print(f' - Default quote is "{quote["quote"]}" - {quote["author"]}')

    ##### test get_weather_forecast() #####
    # print('\nTesting weather forecast retrieval...')

    forecast = get_weather_forecast() # get forecast for default location
    if forecast:
        print(f'\n------ Weather forecast for {forecast["city"]}, {forecast["country"]} ------')
        for period in forecast['periods']:
            print(f' - {period["timestamp"]} | {period["temp"]}°C | {period["description"]}')

    # austin = {'lat': 30.2748,'lon': -97.7404} # coordinates for Texas State Capitol
    # forecast = get_weather_forecast(coords = austin) # get Austin, TX forecast
    # if forecast:
    #     print(f'\nWeather forecast for {forecast["city"]}, {forecast["country"]} is...')
    #     for period in forecast['periods']:
    #         print(f' - {period["timestamp"]} | {period["temp"]}°C | {period["description"]}')

    # invalid = {'lat': 1234.5678 ,'lon': 1234.5678} # invalid coordinates
    # forecast = get_weather_forecast(coords = invalid) # get forecast for invalid location
    # if forecast is None:
    #     print('Weather forecast for invalid coordinates returned None')