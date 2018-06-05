"""
    The Term generator collects toots from the database and generates terms in the terms database
"""
import sqlite3
import datetime
import time

from TootProcessor import TootProcessor

toot_processor = TootProcessor()
from_date = None



with sqlite3.connect("data/toots.db") as conn:
    conn.execute("DROP TABLE IF EXISTS terms")
    conn.execute(
        """
    CREATE TABLE terms (
      created_at DATETIME,
      term TEXT

    )"""
    )
    curs = conn.cursor()
    while True:
        print("TERM_GENERATOR Generating terms")
        if from_date is None:
            curs = curs.execute("SELECT created_at, added_at, content FROM raw_toots WHERE language = 'en'")
            toots = curs.fetchall()
        else:
            curs = conn.execute("SELECT created_at, added_at, content FROM raw_toots WHERE added_at > ? AND language = 'en' ORDER BY added_at", (from_date,))
            toots = curs.fetchall()
        output = []
        for created, added, contents in toots:
            terms = toot_processor.processToot(contents)
            output += [(created, term) for term in terms]

        # If there are any new terms, remember the added_at date of the last one as out new starting point
        if len(output) > 0:
            from_date = added
        print("TERM_GENERATOR_COMPLETE Generated %d terms"%(len(output)))
        curs = curs.executemany("INSERT INTO terms VALUES (?,?)", output)
        conn.commit()

        time.sleep(60)
