"""
 Helper Methods
"""
# pylint: disable-msg=C0103
from threading import Thread
import random
import bisect
from collections import Counter
from functools import reduce
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt

THREADS = 30

def remove_special_char(regex, string):
    """removes any character than a-z and 0-9"""
    return regex.sub('', string.lower())


def read_file_content(file_path):
    """ open given file, read and return the content
    None will be returned if error while opening the file
    """
    content = None
    with open(file_path, 'r+') as f:
        content = f.read()
    return content


def chunks(lis, num):
    """ returns the chunks """
    n = max(1, num)
    return (lis[i:i+n] for i in range(0, len(lis), n))


def save_file(file_name, content):
    """ writes to the file"""
    with open(file_name, 'w+') as f:
        f.write(content)
    print("{} written sucessfully".format(file_name))


def cal_probability(list_of_touple):
    """ calculates the probability each key from given list"""
    total = reduce(lambda x, y: x + y[1], list_of_touple, 0)
    return[{x[0]: x[1]/total} for x in list_of_touple]


def cal_cum_frequency(input_list_of_dict):
    """ calculates the cumulative frequency"""
    list_of_dict = deepcopy(input_list_of_dict)
    for index, obj in enumerate(list_of_dict, start=1):
        req_dicts = list_of_dict[:index]
        total = 0
        for req_dict in req_dicts:
            for key in req_dict.keys():
                if key != 'cum_freq':
                    total += req_dict[key]
        obj['cum_freq'] = total
    return list_of_dict


def _generate_text(char_count, keys, keys_cdfs, result, index):
    """ generate text using thread"""
    characters = []
    for x in range(0, char_count // THREADS):
        randomValue = random.random()
        idx = bisect.bisect(keys_cdfs, randomValue)
        characters.append(keys[idx])
    text = "".join(characters)
    result[index] = text
    print("Generating text in threads")
    return text

def gen_random_text(char_count, keys, keys_cdfs):
    """ generate random text"""
    print("char count", char_count)
    threads = [None] * THREADS
    results = {}
    i = 0
    for i in range(0, len(threads)):
        threads[i] = Thread(target=_generate_text, args=(char_count, keys, keys_cdfs, results, i))
        threads[i].start()

    for thread in threads:
        thread.join()

    return ''.join(list(results.values()))


def get_word_with_probability(text):
    """retun words with its probability"""
    freq_each_words = Counter(text.split()).most_common()
    sum_of_total_char_occ = sum([frequency for (key, frequency) in freq_each_words])
    prob_each_word = {}
    for (key, frequency) in freq_each_words:
        prob_each_word[key] = frequency / sum_of_total_char_occ
    return prob_each_word


def draw_plot(listElements_S, listElements_Z, listElements_U, xLabel, yLabel):
    """ draws the plot"""
    x_S = [x for x in range(1, len(listElements_S) + 1)]
    y_S = np.array(listElements_S)
    x_Z = [x for x in range(1, len(listElements_Z)+1)]
    y_Z = np.array(listElements_Z)
    x_U = [x for x in range(1, len(listElements_U)+1)]
    y_U = np.array(listElements_U)
    plt.figure(figsize=(12, 9))
    plt.plot(x_S, y_S, 'r', label="Simple English")
    plt.plot(x_Z, y_Z, 'b', label="Zips Distribution Words")
    plt.plot(x_U, y_U, 'g', label="Uniform Distribution Words")

    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.yscale('log')
    plt.xscale('log')
    plt.legend(loc='upper right')
    plt.grid()
    plt.show()


def draw_cdf_plot(listElements_S, listElements_Z, listElements_U, xLabel, yLabel):
    """draws the cdf plot"""
    x_S = [x for x in range(1, len(listElements_S) + 1)]
    y_S = np.array(listElements_S)
    x_Z = [x for x in range(1, len(listElements_Z) + 1)]
    y_Z = np.array(listElements_Z)
    x_U = [x for x in range(1, len(listElements_U) + 1)]
    y_U = np.array(listElements_U)
    plt.figure(figsize=(12,9))
    plt.plot(x_S, y_S , 'r', label="Simple English")
    plt.plot(x_Z, y_Z , 'b', label="Zips Distribution Words")
    plt.plot(x_U, y_U , 'g', label="Uniform Distribution Words")

    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.xscale('log')
    plt.yscale('log')
    plt.ylim(0, 1.2)
    plt.legend(loc='bottom right')
    plt.grid()
    plt.show()

