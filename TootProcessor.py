import lxml.html
import re

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

'''Toot Processor Class.'''

class TootProcessor:
    def __init__(self, lemmatize_words = True, remove_duplicates = False):
        self.lemmatizer = WordNetLemmatizer()
        self.lemmatize_words = lemmatize_words
        self.remove_duplicates = remove_duplicates

    def __stripToot(self, toot):
        '''Strip HTML Tags'''
        document = lxml.html.document_fromstring(toot)
        raw_toot = document.text_content()

        '''Strip URLs'''
        raw_toot = re.sub(r"http\S+", "", raw_toot)

        return raw_toot

    def __tokenize(self, raw_toot):
        '''Tokenize Toots: Convert Toot to lowercase, split into words and remove punctuation, remove English stopwords.'''
        raw_toot = raw_toot.lower()

        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(raw_toot)
        tokens = filter(lambda token: token not in stopwords.words('english'), tokens)

        return list(tokens)

    def __lemmatize(self, tokens):
        '''Lemmatize (stemming)'''
        return [self.lemmatizer.lemmatize(t) for t in tokens]
    
    def __removeDuplicates(self, tokens):
        '''Remove Duplicates'''
        return list(set(tokens))
    
    def processToot(self, toot):
        '''Process Toot'''
        raw_toot = self.__stripToot(toot)
        tokens = self.__tokenize(raw_toot)
        
        if self.lemmatize_words:
            tokens = self.__lemmatize(tokens)
            
        if self.remove_duplicates:
            tokens = self.__removeDuplicates(tokens)
        
        return tokens