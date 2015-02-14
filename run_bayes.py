import sys
from load_reviews import load_words, load_reviews 
from naive_bayes import naive_bayes, classifier_stats


def main(argv):
	if len(argv) != 2:
		print 'Give category and quantity.'
		sys.exit(2)
	category = argv[0]
	quantity = argv[1]
	# load data
	try:
		(pos_words, neg_words) = load_words(category, quantity)
	except Exception:
		print("The data for this category and quantity are not found.")
		sys.exit(2)
	# train classifier
	(classifier, train_set, test_set) = naive_bayes(pos_words, neg_words, 3./4.)
	# classifier statistics
	classifier_stats(classifier, test_set)

if __name__ == "__main__":
   main(sys.argv[1:])