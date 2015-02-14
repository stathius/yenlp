import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from sklearn import cross_validation

def naive_bayes(pos_samples, neg_samples, n_folds = 2):
    '''Trains a naive bayes classifier with NLTK. It uses stratified 
    n-fold validation. Inputs are the positive and negative samples and 
    the number of folds. Returns the total accuracy and the classifier and 
    the train/test sets of the last fold.'''
    samples = pos_samples + neg_samples
    labels = [label for (words, label) in samples]
    cv = cross_validation.StratifiedKFold(labels, n_folds= n_folds, shuffle=True)
    
    print "%s-fold stratified cross-validation on %s samples" % (n_folds, len(samples))
    accuracy = 0.0
    for traincv, testcv in cv:
        train_samples = samples[traincv[0]:traincv[len(traincv)-1]]
        test_samples = samples[testcv[0]:testcv[len(testcv)-1]]
        classifier = nltk.NaiveBayesClassifier.train(train_samples)
        accuracy += nltk.classify.util.accuracy(classifier, test_samples)
    accuracy /= n_folds
    print "accuracy: ", accuracy
    return (accuracy, classifier, train_samples, test_samples)

def classifier_stats(classifier, test_samples):
    '''Prints precision/recall statistics of a NLTK classifier'''
    import collections
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)

    for i, (sample, label) in enumerate(test_samples):
        refsets[label].add(i)
        observed = classifier.classify(sample)
        testsets[observed].add(i)

    print 'pos precision:', nltk.metrics.precision(refsets['pos'], testsets['pos'])
    print 'pos recall:', nltk.metrics.recall(refsets['pos'], testsets['pos'])
    print 'pos F-measure:', nltk.metrics.f_measure(refsets['pos'], testsets['pos'])
    print 'neg precision:', nltk.metrics.precision(refsets['neg'], testsets['neg'])
    print 'neg recall:', nltk.metrics.recall(refsets['neg'], testsets['neg'])
    print 'neg F-measure:', nltk.metrics.f_measure(refsets['neg'], testsets['neg'])