import sys
from load_samples import load_samples
from load_samples import whole_text
from sentiwordnet import sentiwordnet_classify


def main(argv):
    if len(argv) != 2:
        print 'usage: python sentiwordnet <category> <quantity>'
        sys.exit(2)
    category = argv[0]
    quantity = int(argv[1])

    print "Category: '%s'" % category
    print "SentiWordNet classification on %s samples\n" % (quantity * 2)

    try:
        (pos_reviews, neg_reviews) = load_samples(category, quantity, whole_text)
    except Exception:
        print("The data for this category and quantity are not found.")
        sys.exit(2)

    reviews = pos_reviews + neg_reviews
    truth = [review[1] for review in reviews]

    predictions = [sentiwordnet_classify(review[0]) for review in reviews]
    accuracy = sum([1 if predictions[i] == truth[i] else 0 
                    for i in range(len(truth))]) / float(len(truth))

    print "Accuracy: %s\n" % accuracy
    print "\n"

if __name__ == "__main__":
   main(sys.argv[1:])