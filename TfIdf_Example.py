from TfIdf import TfIdf

'''Example without DB connection'''

historical_toots = ['hello', 'world', 'lorem', 'ipsum', 'dolor', 'sit', 'amet']
recent_toots = ['hello', 'potato']

tfidf = TfIdf(historical_toots, recent_toots)

print(tfidf.returnScores())

'''Example with DB connection'''

import sqlite3
conn = sqlite3.connect('example.db')

tfidf = TfIdf()
tfidf.setDocumentCountFromDb(conn, "2018-03-0512:00", "2018-06-0512:00") #Historical Toots
tfidf.setTermCountFromDb(conn, "2018-06-0512:00", "2018-06-0514:00") #Recent Toots

print(tfidf.returnScores())