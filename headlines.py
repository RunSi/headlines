#! /usr/bin/env python3

import feedparser
from flask import Flask
from flask import render_template
from flask import request
import json
import requests


app = Flask(__name__)

CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=f892740c6b8545debb27f65024e22d32"
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=801ae403b903e2c9dc811da3189cd032"

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

DEFAULTS = {'publication':'bbc',
            'city': 'London,UK',
            'currency_from': 'GBP',
            'currency_to': 'USD'}

@app.route("/")
#@app.route("/<publication>")

# def bbc():
#     return get_news('bbc')

# @app.route("/cnn")
# def cnn():
#     return get_news('cnn')

# @app.route("/fox")
# def fox():
#     return get_news("fox")


def home():
    # get customized headlines, based on user input or default
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    # get customized weather based on user input or default
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    # get customized currency based on user input or default
    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate, currencies = get_rate(currency_from, currency_to)
    return render_template("home.html", Headlines=publication.upper() + " Headlines", articles=articles,
                           weather=weather,currency_from=currency_from, currency_to=currency_to, rate=rate, currencies=sorted(currencies))



def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']
    #first_article = feed['entries'][0]


    #return render_template("home.html",Headlines = publication.upper() + " Headlines", article=first_article)

    #return render_template("home.html",Headlines = publication.upper() + " Headlines", title=first_article.get("title"),published=first_article.get("published"),summary=first_article.get("summary"))
    # return '''<html>
    # <body>
    #     <h1> {0} Headlines </h1>
    #     <b>{1}</b> <br/>
    #     <i>{2}</i> <br/>
    #     <p>{3}</p> <br/>
    # </body>
    # </html>'''.format(publication.upper(),first_article.get("title"), first_article.get("published"), first_article.get("summary"))

def get_weather(query):
    url = WEATHER_URL.format(query)
    data = requests.get(url)
    parsed = json.loads(data.text)
    weather = None
    if parsed.get("weather"):
        weather = {"description":parsed["weather"][0]["description"],"temperature":parsed["main"]["temp"],"city":parsed["name"],'country': parsed['sys']['country']
                  }
    return weather


def get_rate(frm, to):
    all_currency = requests.get(CURRENCY_URL)

    parsed = json.loads(all_currency.text).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate / frm_rate, parsed.keys())

if __name__ == '__main__':
    app.run(port=5000, debug=True)

