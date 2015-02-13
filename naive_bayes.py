import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
 
def naive_bayes(pos_samples, neg_samples, ratio):
    '''Trains a naive bayes classifier with NLTK.
    Input the positive and negative samples and a given train/test ratio.
    Returns the classifier and the train/test sets.'''
    neg_cutoff = int(len(neg_samples) * ratio)
    pos_cutoff = int(len(pos_samples) * ratio)

    train_samples = neg_samples[:neg_cutoff] + pos_samples[:pos_cutoff]
    test_samples  = neg_samples[neg_cutoff:] + pos_samples[pos_cutoff:]
    print 'train on %d instances, test on %d instances' % (len(train_samples), len(test_samples))

    return (NaiveBayesClassifier.train(train_samples), train_samples, test_samples)

def get_classifier_stats(classifier, test_samples):
    '''Prints statistics of a NLTK classifier'''
    print 'accuracy:', nltk.classify.util.accuracy(classifier, test_samples)
    classifier.show_most_informative_features()
    
    import collections
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)

    for i, (feats, label) in enumerate(testfeats):
        refsets[label].add(i)
        observed = classifier.classify(feats)
        testsets[observed].add(i)

    print 'pos precision:', nltk.metrics.precision(refsets['pos'], testsets['pos'])
    print 'pos recall:', nltk.metrics.recall(refsets['pos'], testsets['pos'])
    print 'pos F-measure:', nltk.metrics.f_measure(refsets['pos'], testsets['pos'])
    print 'neg precision:', nltk.metrics.precision(refsets['neg'], testsets['neg'])
    print 'neg recall:', nltk.metrics.recall(refsets['neg'], testsets['neg'])
    print 'neg F-measure:', nltk.metrics.f_measure(refsets['neg'], testsets['neg'])