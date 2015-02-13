#Small script to get categories out of the business json
#from Yelp Challenge dataset
#It will be used to identify restaurant business ids that will 
#subsequently be used to extract restaurant related reviews
import json

business_fn = 'yelp_academic_dataset_business.json'
reviews_fn = 'yelp_academic_dataset_review.json'

def get_bussiness_ids(category):
	with open(business_fn) as businesses:
		business_ids = []
		for business in businesses:
			business = json.loads(business)
			if category in business['categories']:
				business_ids.append(business['business_id'])
	return business_ids


def save_reviews(category, business_ids, quantity):
	pos_fn = 'yelp_' + category.lower() + '_reviews_%s_pos.json' % quantity
	neg_fn = 'yelp_' + category.lower() + '_reviews_%s_neg.json' % quantity
	pos_file = open(pos_fn, 'w')
	neg_file = open(neg_fn, 'w')

	cnt_pos = 0;
	cnt_neg = 0;
	with open(reviews_fn) as reviews:
		for review in reviews:
			# stop when quantity is reached
			if (cnt_pos >= quantity and cnt_neg >= quantity):
				print "reached\n"
				return None
			review = json.loads(review)
			if review['business_id'] in business_ids:
				#discard 3 star ratings
				if int(review['stars']) > 3 and cnt_pos < quantity:
					print >> pos_file, review
					cnt_pos += 1
				elif int(review['stars']) < 3 and cnt_neg < quantity:
					print >> neg_file, review
					cnt_neg += 1



if __name__ == "__main__":
	category = 'Restaurants'
	business_ids = get_bussiness_ids(category)
	save_reviews(category, business_ids, 1000)
	print "end\n"