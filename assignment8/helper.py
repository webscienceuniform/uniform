""" Helper file for assignment 8"""
import re
import math
from collections import Counter
import numpy as np

def split_with_space(text):
    """ Split given text with spaces """
    text = re.sub(r'[^A-Za-z0-9\s]+', '', text.lower())
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


def tfidf(term_freq, total_doc, match_doc):
    """ Calculates term frequency inverse document frequency"""
    return term_freq * math.log((total_doc/match_doc))


def calculate_cosine_similarity(tfid_dict_1, tfid_dict_2):
    """ Calculates cosines similarity"""
    product = 0
    for term in tfid_dict_1:
        if term in tfid_dict_2.keys():
            product = product + (tfid_dict_1[term] * tfid_dict_2[term])
    ecu_dic_tf1 = np.sum(np.square(list(tfid_dict_1.values())))
    ecu_dic_tf2 = np.sum(np.square(list(tfid_dict_2.values())))
    return product / (ecu_dic_tf1 * ecu_dic_tf2)



