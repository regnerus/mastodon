from collections import Counter
import operator
import numpy as np
import math

'''DfIdf Class.'''

class TfIdf:
    def __init__(self, historical_toots = [], recent_toots = []):
        self.document_count = Counter(historical_toots)
        self.term_count = Counter(recent_toots)

    def __tfidfFunc(self, term):
        tf = self.term_count[term]
        idf = 1.0 / (self.scaling_factor + self.document_count[term])

        return term, tf * idf  # Add one smoothing to avoid division by zero.

    def __getDbTerms(self, conn, datetime_from, datetime_to):
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        ret = c.execute("SELECT term FROM terms WHERE created_at BETWEEN ? AND ?", (datetime_from, datetime_to)).fetchall()
        # print(len(ret))
        return ret

    def setDocumentCount(self, historical_toots):
        self.document_count = Counter(historical_toots)

    def setTermCount(self, recent_toots):
        self.term_count = Counter(recent_toots)

    def setDocumentCountFromDb(self, conn, datetime_from, datetime_to):
        self.document_count = Counter(self.__getDbTerms(conn, datetime_from, datetime_to))

    def setTermCountFromDb(self, conn, datetime_from, datetime_to):
        self.term_count = Counter(self.__getDbTerms(conn, datetime_from, datetime_to))

    def returnScores(self):
        self.scaling_factor = sum(self.document_count.itervalues()) * 1.0 / sum(self.term_count.itervalues()) * 1.0
        self.scaling_factor = self.scaling_factor * 4
        print("Scaling Factor", self.scaling_factor)

        self.tfidf_values = list(map(self.__tfidfFunc, self.term_count))
        self.tfidf_values.sort(key=operator.itemgetter(1), reverse=True)

        return self.tfidf_values

    def printnScores(self, n = 10):
        tfidf_scores = self.returnScores()[0:n]
        for r in tfidf_scores:
            term = r[0]
            print(term, self.term_count[term], self.document_count[term])

