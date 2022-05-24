import os
from urllib import request
import json
from json import loads
import requests
from requests import get
import datetime
from dotenv import load_dotenv
import pandas as pd
import pprint

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
                        
        
        return forecast

    except Exception as e:
        print("\nThere are issues when generating today's weather forecast",e)        

"""
Retrieve the current football matches
"""
def matches():
    try:
        uri = 'https://api.football-data.org/v4/matches'
        headers = { 'X-Auth-Token': api2 }
        response = (requests.get(uri, headers=headers)).json()

        for match in response['matches']:
            Date = match.get('utcDate')
            Away = match.get('awayTeam')
            Home = match.get('homeTeam')
            Duration = match.get('score')
            Hgoal = match.get('score',{}).get('fullTime', {}).get('home')
            Agoal = match.get('score',{}).get('fullTime', {}).get('away')
            Hgoali = match.get('score',{}).get('halfTime', {}).get('home')
            Agoali = match.get('score',{}).get('halfTime', {}).get('away')
            print(Away['shortName'], "VS", Home['shortName'], " ", Date,"Game Duration:", Duration['duration'], "\nFulltime Score=>", Hgoal,":",Agoal, " ", " Halftime Score=>", Hgoali,":",Agoali,"\n")
            
        
    except Exception as e:
        print(" Sorry, We couldn't get today's match", e)

"""
Retrieve the summary extract for a random Wikipedia article.
"""
def get_wikipedia_article():
    try: # retrieve random Wikipedia article
        data = json.load(request.urlopen('https://en.wikipedia.org/api/rest_v1/page/random/summary'))
        return {'title': data['title'],
                'extract': data['extract'],
                'url': data['content_urls']['desktop']['page']}

    except Exception as e:
        print(e)


if __name__ == '__main__':
   
    print("------ Quote of the day ------\n")
    print(get_quotes())

    forecast = get_weather_forecast() # get forecast for default location
    if forecast:
        print(f'\n\n------ Weather forecast for {forecast["city"]}, {forecast["country"]} ------\n')
        for period in forecast['periods']:
            print(f' - {period["timestamp"]} | {period["temp"]}°C | {period["description"]}')

    print("\n\n---Football matches---\n")
    print(matches())

    

    article = get_wikipedia_article()
    if article:
        print(f'\n{article["title"]}\n<{article["url"]}>\n{article["extract"]}')