from nltk.corpus import wordnet as wordnet
from nltk.corpus import sentiwordnet as swn
import nltk

def wordnet_pos_code(tag):
    '''Translation from nltk tags to Wordnet code'''
    if tag.startswith('NN'):
        return wordnet.NOUN
    elif tag.startswith('VB'):
        return wordnet.VERB
    elif tag.startswith('JJ'):
        return wordnet.ADJ
    elif tag.startswith('RB'):
        return wordnet.ADV
    else:
        return ''

def pos_tag(text):
    '''POS tagging of a text'''
    sentences = nltk.sent_tokenize(text)
    tagged_words = []
    for sentence in sentences:
        tokens = nltk.word_tokenize(sentence)
        tag_tuples = nltk.pos_tag(tokens)
        for (string, tag) in tag_tuples:
            token = {'word':string, 'pos':tag}            
            tagged_words.append(token)    
    return tagged_words

def word_sense_cdf(word, context, wn_pos):
    '''Word sense disambiguation in terms of matching words frequency 
    between the context each sense's definition. Adapted from
    www.slideshare.net/faigg/tutotial-of-sentiment-analysis'''
    senses = wordnet.synsets(word, wn_pos)
    if len(senses) > 0:
        cfd = nltk.ConditionalFreqDist((sense, def_word)
                       for sense in senses
                       for def_word in sense.definition().split()
                       if def_word in context)
        best_sense = senses[0]
        for sense in senses:
            try:
                if cfd[sense].max() > cfd[best_sense].max():
                    best_sense = sense
            except: 
                pass                
        return best_sense
    else:
        return None

def word_sense_similarity(word, context, dummy = None):
    '''Another word sense disambiguation technique. It's VERY SLOW.
    Adapted from: pythonhosted.org/sentiment_classifier'''
    wordsynsets = wordnet.synsets(word)
    bestScore = 0.0
    result = None
    for synset in wordsynsets:
        for w in nltk.word_tokenize(context):
            score = 0.0
            for wsynset in wordnet.synsets(w):
                sim = wordnet.path_similarity(wsynset, synset)
                if(sim == None):
                    continue
                else:
                    score += sim
            if (score > bestScore):
                bestScore = score
                result = synset
    return result

def sentiwordnet_classify(text, wsd = word_sense_cdf):
    '''Classifies a text according to the sentiment analysis based
    on SentiWordNet.'''
    tagged_words = pos_tag(text)

    obj_score = 0 # object score 
    pos_score=0 # positive score
    neg_score=0 #negative score
    pos_score_tre=0
    neg_score_tre=0
    threshold = 0.75

    for word in tagged_words:
    #     print word
        if 'punct' not in word :
            sense = wsd(word['word'], text, wordnet_pos_code(word['pos']))
            if sense is not None:
                sent = swn.senti_synset(sense.name())
                if sent is not None and sent.obj_score() <> 1:
                    obj_score = obj_score + float(sent.obj_score())
                    pos_score = pos_score + float(sent.pos_score())
                    neg_score = neg_score + float(sent.neg_score())
                    if sent.obj_score() < threshold:
                        pos_score_tre = pos_score_tre + float(sent.pos_score())
                        neg_score_tre = neg_score_tre + float(sent.neg_score())

    #Trust the thresholded value more when classifying
    if pos_score_tre != 0 or neg_score_tre !=0:
        clss = 'pos' if pos_score_tre > neg_score_tre else 'neg'
    elif pos_score != 0 or neg_score !=0:
        clss = 'pos' if pos_score > neg_score else 'neg'
    else:
        clss = None
        
    return clss