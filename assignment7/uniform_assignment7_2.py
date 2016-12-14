"""
 Generative Model
"""
# pylint: disable-msg=C0103
import re
import threading
from timeit import default_timer as timer
from pathlib import Path
from collections import Counter
from operator import itemgetter
import numpy as np
from helper import read_file_content
from helper import chunks
from helper import remove_special_char
from helper import save_file
from helper import cal_cum_frequency
from helper import draw_plot
from helper import gen_random_text
from helper import get_word_with_probability
from helper import draw_cdf_plot


counter = Counter()
total_character_in_english_text = 0
probabilities_file = 'probabilities.py.txt'
regex = re.compile('[^a-zA-Z0-9 ]')

def cdf_calculaton(prob_dict):
    """ calculates cdf"""
    arr_for_cdf = list(prob_dict.values())
    a = np.array(arr_for_cdf)
    cdfEvalDict = np.cumsum(a)
    return (list(prob_dict.keys()), cdfEvalDict)

def count_alphanumberic(string):
    """ count frequency of each alphabet"""
    global counter
    clean_string = remove_special_char(regex, string)
    ctr = Counter(clean_string)
    counter = counter + ctr

def perform_kolmogro_test(cdf_main , cdf_compare):
    """ perform kolmogro test"""
    max_point_wise_distance = max([abs(cdf_S - cdf_Zipf) \
                                 for (cdf_S, cdf_Zipf) in \
                                                zip(cdf_main, cdf_compare)])
    return max_point_wise_distance

def process_articles(articles):
    """ access all the article from articles"""
    for article in articles:
        count_alphanumberic(article)


def use_multithread(articles):
    """" using multi threading"""
    group_articles = chunks(articles, int(len(articles) / 20))
    thread_list = []
    for art in group_articles:
        t = threading.Thread(target=process_articles, args=(art, ))
        thread_list.append(t)
        t.start()

    for thread in thread_list:
        thread.join()


def without_multi(articles):
    """ processing in single thread"""
    for article in articles:
        count_alphanumberic(article)


def process_output_file(file_path):
    """ read already generated output and process it"""
    global counter
    output = None
    with file_path.open() as f:
        output = f.read()
    counter = eval(output)


def load_file_and_process(file_path):
    """ load the simple article file and process it"""
    global counter
    content = read_file_content(file_path)
    start = timer()
    articles = content.split("\n")
    use_multithread(articles)
    end = timer()
    print("Total time taken:", end - start)
    # sorting the counter
    counter = sorted(counter.items(), key=itemgetter(0))
    save_file('output.txt', str(counter))


def process_given_info_file(file_path):
    """ process the given file which contains probability information"""
    def get_text(text, start, end):
        """ returns slice of text from stat to end:"""
        return text[text.find(start): text.find(end) + 1]

    def process_list(given_list):
        """ returns dict"""
        return list([{x[0]: x[1]} for x in given_list])
    file_content = read_file_content(file_path)
    text_arr = file_content.split("\n")
    texts = list(filter(lambda x: len(x.strip()) > 0, text_arr))
    result = list(map(lambda x: get_text(x, '{', '}'), texts))
    final = []
    for res in result:
        jt = eval(res)
        mp = sorted(jt.items(), key=itemgetter(0))
        final.append(mp)
    return list(map(lambda x: process_list(x), final))



def get_keys_and_cdfs(list_of_dict):
    """ returns the keys and its cumulative frequency"""
    cums = []
    keys = []
    for cur_dict in list_of_dict:
        for key in cur_dict.keys():
            if key == 'cum_freq':
                cums.append(cur_dict[key])
            else:
                keys.append(key)
    return [keys, cums]


def main(file_path):
    """ entry point of the application"""
    global total_character_in_english_text
    simple_english_text = read_file_content(file_path)
    total_character_in_english_text = len(simple_english_text)
    prob_each_word_dict = get_word_with_probability(simple_english_text)
    _, assoc_cdf_s = cdf_calculaton(prob_each_word_dict)

    # for Zipf and uniform distrubation
    prob_dist_given = process_given_info_file(probabilities_file)
    zipf_cum = cal_cum_frequency(prob_dist_given[0])
    unif_cum = cal_cum_frequency(prob_dist_given[0])
    all_keys_zipf, asso_zipf_cum = get_keys_and_cdfs(zipf_cum)
    all_keys_unif, asso_unif_cum = get_keys_and_cdfs(unif_cum)

    text_zipf = gen_random_text(total_character_in_english_text, all_keys_zipf, asso_zipf_cum)
    save_file('text_zipf.txt', text_zipf)

    text_unif = gen_random_text(total_character_in_english_text, all_keys_unif, asso_unif_cum)
    save_file('text_unif.txt', text_unif)

    prob_for_each_ord_dict_zipf = get_word_with_probability(text_zipf)
    _, ass_cdf_new_zipf = cdf_calculaton(prob_for_each_ord_dict_zipf)

    prob_for_each_word_dict_unif = get_word_with_probability(text_unif)
    _, asso_cdf_new_unif = cdf_calculaton(prob_for_each_word_dict_unif)
    #--------------------------------------------------------------------------
    # Plots for Rank Frequency STARTS
    #--------------------------------------------------------------------------
    #Note: _S is for simple English
    freq_each_word_s = Counter(simple_english_text.split()).most_common()
    list_for_rank_freq_diag_s = [freq for (word, freq) in freq_each_word_s]

    #Note _Z is for Zipf
    freq_each_word_z = Counter(text_zipf.split()).most_common()
    list_for_rank_freq_diag_z = [freq for (word, freq) in freq_each_word_z]

    #Note_U is for Uniform
    freq_each_word_u = Counter(text_unif.split()).most_common()
    list_for_rank_freq_diag_u = [freq for (word, freq) in freq_each_word_u]

    draw_plot(list_for_rank_freq_diag_s, list_for_rank_freq_diag_z,\
             list_for_rank_freq_diag_u, "x = Rank", "y = Number of occurences")
    #--------------------------------------------------------------------------
    # Plots for Rank Frequency ENDS
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    # Plots for Rank and CDF STARTS
    #--------------------------------------------------------------------------

    draw_cdf_plot(assoc_cdf_s, ass_cdf_new_zipf, asso_cdf_new_unif,\
     "x = Rank", "y = Cumulative Frequency")

    #--------------------------------------------------------------------------
    # Plots for Rank and CDF ENDS
    #--------------------------------------------------------------------------
    # Now we perform Kolmogorov Smirnov test  by calculating the maximum
    # pointwise distance of CDFs
    max_point_wised_s_zipf = perform_kolmogro_test(assoc_cdf_s, ass_cdf_new_zipf)
    max_point_wised_s_unif = perform_kolmogro_test(assoc_cdf_s, asso_cdf_new_unif)
    print("Obtained Maximum Pointwise Distance between simple English and Zipf is : ", max_point_wised_s_zipf)
    print("Obtained Maximum Pointwise Distance between simple English and Unif is : ", max_point_wised_s_unif)

if __name__ == "__main__":
    file = 'simple-20160801-1-article-per-line'
    main(file)
