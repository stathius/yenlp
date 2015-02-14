import json
import re

template_fn = 'yelp_{category}_reviews_{quantity}_{classif}.json'

def word_class(words):
    return dict([(word, True) for word in words])

def load_words(category, quantity):
    '''Reads a number of pre-extracted reviews for the given category and 
    returns two lists of pos/neg reviews.'''
    pos_reviews = open(template_fn.format(category = category.lower(), 
                                       quantity = quantity, classif = 'pos'), 'r')
    neg_reviews = open(template_fn.format(category = category.lower(), 
                                       quantity = quantity, classif = 'neg'), 'r')
    pos_words = [(word_class(re.findall(r"[\w']+|[.,!?;-]", json.loads(review)['text'])), 'pos') 
                for review in pos_reviews]
    neg_words = [(word_class(re.findall(r"[\w']+|[.,!?;-]", json.loads(review)['text'])), 'neg') 
                for review in neg_reviews]
    return (pos_words, neg_words)

def load_reviews(category, quantity):
    '''Read a number of pre-extracted reviews for a certain category and 
    returns two lists of pos/neg reviews.'''