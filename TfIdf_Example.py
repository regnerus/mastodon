from TfIdf import TfIdf

'''Example without DB connection'''

historical_toots = ['hello', 'world', 'lorem', 'ipsum', 'dolor', 'sit', 'amet']
recent_toots = ['hello', 'potato']

tfidf = TfIdf(historical_toots, recent_toots)

print(tfidf.returnScores())

'''Example with DB connection'''

import sqlite3
conn = sqlite3.connect('data/toots.db')

tfidf = TfIdf()
tfidf.setDocumentCountFromDb(conn, "2018-03-05 12:57:13.048000+00:00", "2018-06-05 12:00:00.000000+00:00") #Historical Toots
tfidf.setTermCountFromDb(conn, "2018-06-05 12:00:00.000000+00:00", "2018-06-05 18:00:00.000000+00:00") #Recent Toots

print(tfidf.returnScores())