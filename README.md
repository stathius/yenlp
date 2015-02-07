##Sentiment Analysis on [Yelp Dataset Challenge](http://www.yelp.com/dataset_challenge)

### Scope 
This is the Final Project for the [Data Mining course](http://www.cs.uoi.gr/~tsap/teaching/cs059/index-en.html) 
taught in the Computer Science & Engineering department of the Univerisity of Ioannina during Fall 2014.
For details checkout the [handout](http://www.cs.uoi.gr/~tsap/teaching/cs059/assignments/project-en.pdf).

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

###Goal

The objective of this project is to apply various sentiment analysis techniques(NLP) on the restaurant reviews and assess 
whether they can correctly identify the reviews as positive or negative. 


### Techniques

Three different techniques will be assesed and compared:

* Training and testing using the dataset 
* Training with generic lexicons
* A pretrained state-of-the-art system

Only a subset of the dataset will be used.

### Training and testing using the data set

Training/testing on the dataset using bag of words and a NaiveBayes classifier...

###Training with generic lexicons

WordNet & SentiWordNet...

###A pretrained state-of-the-art system

Stanford's [CoreNLP](http://nlp.stanford.edu/sentiment/code.html)
