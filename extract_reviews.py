#Small script to get categories out of the business json
#from Yelp Challenge dataset
#It will be used to identify restaurant business ids that will 
#subsequently be used to extract restaurant related reviews
import json

business_fn = 'yelp_academic_dataset_business.json'
reviews_fn = 'yelp_academic_dataset_review.json'
template_fn = 'yelp_{category}_reviews_{quantity}_{classif}.json'


def get_bussiness_ids(category):
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