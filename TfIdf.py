from collections import Counter
import operator

'''DfIdf Class.'''

class TfIdf:
    def __init__(self, historical_toots = [], recent_toots = []):
        self.document_count = Counter(historical_toots)
        self.term_count = Counter(recent_toots)

    def __tfidfFunc(self, term):
        return (term, self.term_count[term] * 1.0 / (1 + self.document_count[term])) # Add one smoothing to avoid division by zero.

    def set_document_count(self, historical_toots):
        self.document_count = Counter(historical_toots)

    def set_term_count(self, recent_toots):
        self.term_count = Counter(recent_toots)

    def return_scores(self):
        self.tfidf_values = list(map(self.__tfidfFunc, self.term_count))
        self.tfidf_values.sort(key=operator.itemgetter(1), reverse=True)     

        return self.tfidf_values