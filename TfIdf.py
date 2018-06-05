from collections import Counter
import operator

'''DfIdf Class.'''

class TfIdf:
    def __init__(self, historical_toots = [], recent_toots = []):
        self.document_count = Counter(historical_toots)
        self.term_count = Counter(recent_toots)

    def __tfidfFunc(self, term):
        return (term, self.term_count[term] * 1.0 / (1 + self.document_count[term])) # Add one smoothing to avoid division by zero.

    def __getDbTerms(self, conn, datetime_from, datetime_to):
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        ret = c.execute("SELECT term FROM terms WHERE created_at BETWEEN ? AND ?", (datetime_from, datetime_to)).fetchall()
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
        self.tfidf_values = list(map(self.__tfidfFunc, self.term_count))
        self.tfidf_values.sort(key=operator.itemgetter(1), reverse=True)     

        return self.tfidf_values