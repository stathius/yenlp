import json
import re
from nltk.corpus import stopwords
import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.tokenize import word_tokenize

template_fn = 'yelp_{category}_reviews_{quantity}_{classif}.json'

def single_words(words):
    '''Simplest filter that returns all the words of the review.'''
    return dict([(word, True) for word in words])
 
def stopword_filtered_words(words):
    '''Returns all the single words after removing the stop words.'''
    stopset = set(stopwords.words('english'))
    return dict([(word, True) for word in words if word not in stopset])

def bigram_words(words, score_fn=BigramAssocMeasures.chi_sq, n=500):
    ''''''
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])

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
    pos_samples = [(filtr(tokenize(json.loads(review)['text'])), 'pos') for review in pos_reviews]
    neg_samples = [(filtr(tokenize(json.loads(review)['text'])), 'neg') for review in neg_reviews]
    return (pos_samples, neg_samples)