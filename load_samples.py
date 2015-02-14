import json
import re
from nltk.corpus import stopwords
import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.tokenize import word_tokenize

template_fn = 'yelp_{category}_reviews_{quantity}_{classif}.json'

def single_words(text):
    '''Simplest filter that returns all the words of a given text.'''
    return dict([(word, True) for word in tokenize(text)])
 
def stopword_filtered_words(text):
    '''Returns all the single words after removing the stop words.'''
    stopset = set(stopwords.words('english'))
    return dict([(word, True) for word in tokenize(text) if word not in stopset])

def bigram_words(text, score_fn=BigramAssocMeasures.chi_sq, n=500):
    '''Find the best n bigrams of a text by means of a give measure.'''
    words = tokenize(text)
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])

def untouched()

def tokenize(text):
    '''Splits a text to words, separates by space and punctuation, 
    converts to lowercase.'''
    return re.findall(r"[\w']+|[.,!?;-]", text)

def load_samples(category, quantity, filtr):
    '''Reads a number of pre-extracted reviews for the given category and 
    returns two lists of pos/neg samples.
    The samples are extracted according to the given filter'''
    pos_reviews = open(template_fn.format(category = category.lower(), 
                                       quantity = quantity, classif = 'pos'), 'r')
    neg_reviews = open(template_fn.format(category = category.lower(), 
                                       quantity = quantity, classif = 'neg'), 'r')
    pos_samples = [(filtr((json.loads(review)['text'])), 'pos') for review in pos_reviews]
    neg_samples = [(filtr((json.loads(review)['text'])), 'neg') for review in neg_reviews]
    return (pos_samples, neg_samples)