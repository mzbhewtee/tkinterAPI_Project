from flask import Flask, render_template
from email.quoprimime import quote
import os
from urllib import request
import json
from json import loads
import requests
from requests import get
import datetime
from datetime import date
from dotenv import load_dotenv
import pandas as pd
import csv

today = date.today()

load_dotenv() 

api = os.environ.get('api')
api2 = os.environ.get('api2')


# x = get_quotes()

app = Flask(__name__)

@app.route("/")


def index():
    '''
    Render the html page
    '''
    try: #retrieve quotes
        response = get('http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en')
        Text = '{quoteText}'.format(**loads(response.text))
        Author = '{quoteAuthor}'.format(**loads(response.text))

    except Exception as e:
        print('Life goes on, no matter your struggles - Beauty Ikudehinbu')
        Text = 'Life goes on, no matter your struggles'
        Author = '- Beauty Ikudehinbu'
        return render_template('index.html', get_quotes=Text, author=Author, wiki=aextract, game=len(games), games=games, len=len(x), x=x, date=date)
     

    coords={'lat': -1.9441, 'lon': 30.0619} # default location at Kigali,
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
                        
        
            if forecast:
                x = []
            # print(f'\n\n------ Weather forecast for {forecast["city"]}, {forecast["country"]} ------\n')
                for period in forecast['periods']:
                    x.append(f'{period["timestamp"]} | {period["temp"]}°C | {period["description"]}')
                    

    except Exception as e:
        print("\nThere are issues when generating today's weather forecast",e)

    
    """
Retrieve the summary extract for a random Wikipedia article.
"""
    try: # retrieve random Wikipedia article
        data = json.load(request.urlopen('https://en.wikipedia.org/api/rest_v1/page/random/summary'))
        article =  {'title': data['title'],
                'extract': data['extract'],
                'url': data['content_urls']['desktop']['page']}
        if article:
            title = article['title']
            aurl = article['url']
            aextract = article['extract']

            # return(f'{article["title"]}   {article["url"]}   {article["extract"]}')
    except Exception as e:
        print(e)


    try:
        uri = 'https://api.football-data.org/v4/matches'
        headers = { 'X-Auth-Token': api2 }
        response = (requests.get(uri, headers=headers)).json()
        
        games = []

        for match in response['matches']:
            Date = match.get('utcDate')
            Away = match.get('awayTeam')
            Home = match.get('homeTeam')
            Hgoal = match.get('score',{}).get('fullTime', {}).get('home')
            Agoal = match.get('score',{}).get('fullTime', {}).get('away')
            
            games.append(f' {Date} {Away["shortName"]} {Hgoal} 🆚 {Agoal} {Home["shortName"]}')

            

    except Exception as e:
        print(" Sorry, We couldn't get today's match", e)   

    ml = []
    date = today.strftime("%B %d, %Y")

    with open('static/ML.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
    
        for row in reader:
            p = row['PROJECT']
            d = row['DETAILS']
            ml.append(f'{p} {d}')

        


    return render_template('index.html', get_quotes=Text, author=Author, wiki=aextract, game=len(games), games=games, len=len(x), x=x, date=date, title=title, aurl=aurl, mls=len(ml), ml=ml)
     

if __name__ == "__main__":
    app.run(debug=True)