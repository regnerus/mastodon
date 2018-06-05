from TfIdf import TfIdf

historical_toots = ['hello', 'world', 'lorem', 'ipsum', 'dolor', 'sit', 'amet']
recent_toots = ['hello', 'potato']

tfidf = TfIdf(historical_toots, recent_toots)

print(tfidf.return_scores())