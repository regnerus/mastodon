from TfIdf import TfIdf

'''Example with DB connection'''

import sqlite3
conn = sqlite3.connect('data/toots.db')

# tfidf = TfIdf()
# tfidf.setDocumentCountFromDb(conn, "2018-03-05 12:57:13.048000+00:00", "2018-06-10 18:00:00.000000+00:00") #Historical Toots
# tfidf.setTermCountFromDb(conn, "2018-06-10 18:00:00.000000+00:00", "2018-06-15 00:00:00.000000+00:00") #Recent Toots


# print(tfidf.printnScores())

tfidf = TfIdf()
tfidf.setDocumentCountFromDb(conn, "2018-03-05 12:57:13.048000+00:00", "2018-06-15 00:00:00.000000+00:00") #Historical Toots
tfidf.setTermCountFromDb(conn, "2018-06-06 08:00:00.000000+00:00", "2018-06-07 08:00:00.000000+00:00") #Recent Toots


print(tfidf.printnScores())
# print(tfidf.returnScores())
# print(tfidf.term_count)