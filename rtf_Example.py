from relative_term_frequency import RelativeTermFrequency

'''Example with DB connection'''

import sqlite3
conn = sqlite3.connect('data/toots.db')

# rtf = RelativeTermFrequency()
# rtf.setDocumentCountFromDb(conn, "2018-03-05 12:57:13.048000+00:00", "2018-06-10 18:00:00.000000+00:00") #Historical Toots
# rtf.setTermCountFromDb(conn, "2018-06-10 18:00:00.000000+00:00", "2018-06-15 00:00:00.000000+00:00") #Recent Toots


# print(rtf.printnScores())

rtf = RelativeTermFrequency()
rtf.setDocumentCountFromDb(conn, "2018-03-05 12:57:13.048000+00:00", "2018-06-15 00:00:00.000000+00:00") #Historical Toots
rtf.setTermCountFromDb(conn, "2018-06-10 08:00:00.000000+00:00", "2018-06-11 08:00:00.000000+00:00") #Recent Toots


print(rtf.printnScores())
rtf.tablePrintScores(5)
# print(rtf.returnScores())
# print(rtf.term_count)