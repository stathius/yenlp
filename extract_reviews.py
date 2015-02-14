#Small script to get categories out of the business json
#from Yelp Challenge dataset
import json
import sys

business_fn = 'yelp_academic_dataset_business.json'
reviews_fn = 'yelp_academic_dataset_review.json'
template_fn = 'yelp_{category}_reviews_{quantity}_{classif}.json'


def get_bussiness_ids(category):
    '''Gets all the (anonynimized)business ids for a given category'''
    with open(business_fn) as businesses:
        business_ids = []
        for business in businesses:
            business = json.loads(business)
            if category in business['categories']:
                business_ids.append(business['business_id'])
    return business_ids


def save_reviews(category, quantity):
    '''Saves the given number of reviews of a specific category to two files, 
    one for each class(pos/neg).'''
    business_ids = get_bussiness_ids(category)
    
    pos_reviews = open(template_fn.format(category = category.lower(), 
                                          quantity = quantity, classif = 'pos'), 'w')
    neg_reviews = open(template_fn.format(category = category.lower(), 
                                          quantity = quantity, classif = 'neg'), 'w')
    cnt_pos = 0;
    cnt_neg = 0;
    with open(reviews_fn) as reviews:
        for review in reviews:
            # stop when quantity is reached
            if (cnt_pos >= quantity and cnt_neg >= quantity):
                return None
            review = json.loads(review)
            if review['business_id'] in business_ids:
                #discard 3 star ratings
                if int(review['stars']) > 3 and cnt_pos < quantity:
                    json.dump(review, pos_reviews)
                    pos_reviews.write('\n')
                    cnt_pos += 1
                elif int(review['stars']) < 3 and cnt_neg < quantity:
                    json.dump(review, neg_reviews)
                    neg_reviews.write('\n')
                    cnt_neg += 1

def main(argv):
    if len(argv) != 2:
        print 'Give category and quantity.'
        sys.exit(2)
    category = argv[0]
    quantity = int(argv[1])
    # load data
    try:
        print "Creating files with %s reviews of the '%s' category" % (quantity, category)
        save_reviews(category, quantity)
    except Exception:
        print("Something went wrong.")
        sys.exit(2)

if __name__ == "__main__":
   main(sys.argv[1:])