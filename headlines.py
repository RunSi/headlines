#! /usr/bin/env python3

import feedparser
from flask import Flask
from flask import render_template

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

@app.route("/")
@app.route("/<publication>")

# def bbc():
#     return get_news('bbc')

# @app.route("/cnn")
# def cnn():
#     return get_news('cnn')

# @app.route("/fox")
# def fox():
#     return get_news("fox")


def get_news(publication='bbc'):
    feed = feedparser.parse(RSS_FEEDS[publication])
    #first_article = feed['entries'][0]
    return render_template("home.html", Headlines=publication.upper() + " Headlines", articles=feed['entries'])

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


if __name__ == '__main__':
    app.run(port=5000, debug=True)

