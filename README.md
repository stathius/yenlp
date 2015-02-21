##Sentiment Analysis on [Yelp Dataset Challenge](http://www.yelp.com/dataset_challenge)

###Goal

The objective of this project is to apply various sentiment analysis techniques(NLP) on the restaurant reviews and assess 
whether they can correctly identify the reviews as positive or negative. 

### Yelp Dataset Challenge

Yelp has released an anonymized part of their stored data to the public. This was accompanied by 
[a challenge] (http://www.yelp.com/dataset_challenge) with various awards in order to incentivize research 
and generate insights for the use of the data. 

Here follows a brief explanation of the dataset, from their website.

```
The Challenge Dataset includes data from Phoenix, Las Vegas, Madison, Waterloo and Edinburgh:

* 42,153 businesses
* 320,002 business attributes
* 31,617 check-in sets
* 252,898 users
* 955,999 edge social graph
* 403,210 tips
* 1,125,458 reviews
```

This project is not a participation in the challenge. 

### Techniques

Three different techniques will be assesed and compared:

* Training and testing using the dataset 
* Training with generic lexicons
* A pretrained state-of-the-art system

Only a subset of the dataset will be used.

### Training and testing using the data set

Training/testing on the dataset using bag of words and a NaiveBayes classifier. 
Three different feature selection where implementes: 
* single words
* single words after removing stopwords
* bigrams

The evaluation of the classifier is done by stratified k-fold cross validation.

###Training with generic lexicons

WordNet & SentiWordNet...

###A pretrained state-of-the-art system

Stanford's [CoreNLP](http://nlp.stanford.edu/sentiment/code.html)

## Usage

A brief explanation on how to run the code.

### Dependencies

Make sure you have the following libraries installed before running the code.

* [NLTK](http://www.nltk.org)
* [Scikit-Learn](http://scikit-learn.org/stable/install.html)

Also you must have installed the *stopword corpora* of NLTK.
To bring up the NLTK downloader, run the following in a python console.

```
import nltk
nltk.download()
```

### Extracting reviews

You need to provide the category of the businesses and the quantity of samples for each review class (pos/neg).
The script creates two json files one for each class.

```
python extract_reviews.py 'Restaurants' 1000
```

### Naive Bayes

You need to provide the category, the number of samples for each class and the number of folds for the k-fold cross validation.
It trains one classifier for each feature extraction filter (single words, stopwords excluded, bigrams) and prints the overall accuracy.

```
python run_bayes 'Restaurants' 1000 2
```


### Scope 
This is a project for the [Data Mining course](http://www.cs.uoi.gr/~tsap/teaching/cs059/index-en.html) taught in the Computer Science & Engineering department of the Univerisity of Ioannina during the fall semester 2014/2015. 
For details checkout the [handout](http://www.cs.uoi.gr/~tsap/teaching/cs059/assignments/project-en.pdf).
