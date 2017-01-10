""" Helper file for assignment 8"""
import re
import math
from collections import Counter
import numpy as np

def split_with_space(text):
    """ Split given text with spaces """
    text = re.sub('[^A-Za-z0-9\s]+', '', text.lower())
    return re.split(r'\s+', text)


def word_set_from_text(text):
    """ Builds set of words from the text"""
    # split the text using space
    words = split_with_space(text)
    tkon = set()
    for word in words:
        tkon.add(word)
    return tkon


def calc_jaccard_similarity(wordset1, wordset2):
    """Calculates jaccard similarity from given sets"""
    intersection = wordset1.intersection(wordset2)
    union = wordset1.union(wordset2)
    return len(intersection) / len(union)


def cal_term_freq(text_document):
    """ Calculate frequency of each word in given document"""
    words = split_with_space(text_document)
    gen_freq = dict(Counter(words))
    return gen_freq
    # length = len(words)
    # for key in gen_freq:
    #     gen_freq[key] = gen_freq[key] / length
    # return gen_freq


def tfidf(term_freq, total_doc, match_doc):
    """ Calculates term frequency inverse document frequency"""
    return term_freq * math.log((total_doc/match_doc))


def calculate_cosine_similarity(tfIdfDict1, tfIdfDict2):
    """ Calculates cosines similarity"""
    scalar_product_article1_article2 = 0
    for each_term_article1 in tfIdfDict1:
        if each_term_article1 in tfIdfDict2.keys():
            scalar_product_article1_article2 = scalar_product_article1_article2 + (tfIdfDict1[each_term_article1] * tfIdfDict2[each_term_article1])

    euc_dist_tfIdfDict1 = np.sum(np.square(list(tfIdfDict1.values())))
    euc_dist_tfIdfDict2 = np.sum(np.square(list(tfIdfDict2.values())))

    cosineSimilarity = scalar_product_article1_article2 / (euc_dist_tfIdfDict1 * euc_dist_tfIdfDict2)
    return cosineSimilarity

    # tf_idf_1 = []
    # tf_idf_2 = []
    # to_iterate = None
    # alter_dict = None

    # if len(tfIdfDict1.keys()) > len((tfIdfDict2)):
    #     to_iterate = tfIdfDict1
    #     alter_dict = tfIdfDict2
    # else:
    #     to_iterate = tfIdfDict2
    #     alter_dict = tfIdfDict1

    # for key, val in to_iterate.items():
    #     tf_idf_1.append(val)
    #     tf_idf_2.append(alter_dict.get(key, 0))



