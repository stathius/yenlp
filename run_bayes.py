import sys
from load_samples import load_samples
from load_samples import single_words
from load_samples import stopword_filtered_words
from load_samples import bigram_words
from naive_bayes import naive_bayes


def main(argv):
    if len(argv) != 3:
        print 'usage: python run_bayes <category> <quantity> <nfolds>'
        sys.exit(2)
    category = argv[0]
    quantity = int(argv[1])
    n_folds = int(argv[2])

    print "Category: '%s'\n" % category
    filters = [single_words, stopword_filtered_words, bigrams, stopword_filtered_bigrams]

    for filt in filters:
        print "Filter: ", filt.__name__
        print "%s-fold stratified cross-validation on %s samples" % (n_folds, quantity * 2)

        try:
            (pos_words, neg_words) = load_samples(category, quantity, filt)
        except Exception:
            print("The data for this category and quantity are not found.")
            sys.exit(2)

        (accuracy, classifier, train_set, test_set) = naive_bayes(pos_words, neg_words, n_folds)
        print "accuracy: %s\n" % accuracy
        classifier.show_most_informative_features()
        print "\n"

if __name__ == "__main__":
   main(sys.argv[1:])