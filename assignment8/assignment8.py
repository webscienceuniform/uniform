# pylint: disable-msg=C0103
""" Assignment Number 8"""
from pathlib import Path
import pandas as pd
from helper import word_set_from_text
from helper import calc_jaccard_similarity
from helper import cal_term_freq
from helper import tfidf
from helper import calculate_cosine_similarity


gen_set_of_docs = None

def gen_word_set(data_frame):
    """ Generate word set for the given data frame"""
    results = []
    for _, row in data_frame.iterrows():
        results.append(word_set_from_text(row.text))
    data_frame['word_set'] = results


def cal_doc_freq_of_term(term, list_of_docs):
    """ Calculates the document frequency of given term """
    # create set from the doc
    # this code seems too slow
    if gen_set_of_docs is None:
        gen_set_of_docs = [word_set_from_text(doc) for doc in list_of_docs]
    result = {term: 0}
    for gen_set in gen_set_of_docs:
        if term in gen_set:
            result[term] += 1
    return result


# For question 1.1.2
def count_freq_each_term_each_article(data_frame):
    """ Calculates the frequency of each term in each article"""
    results = []
    for _, row in data_frame.iterrows():
        results.append(cal_term_freq(row.text))
    data_frame['term_freq'] = results


def document_frequency_of_all_term(input_terms, documents):
    """ Calculate the document frequency of each term in given documents"""
    results = dict()
    for term in input_terms:
        print("Processing ", term)
        result = cal_doc_freq_of_term(term, documents)
        results[term] = result[term]
    return results


def cal_tfidf_each_term(data_frame, document_term_freq):
    """ Calculates the tfidf of each term"""
    results = []
    doc_length = len(data_frame.term_freq)
    for _, row in data_frame.iterrows():
        term_set = row.term_freq
        res = dict()
        for term in term_set:
            res[term] = tfidf(term_set[term], doc_length, document_term_freq[term])
        results.append(res)
    data_frame['tf_idf'] = results


def compare_cosine_for_random_100_column(data_frame, cosine_similarity):
    """ calculate and returns """
    # lets select 100 ids
    sample_data = data_frame.sample(100)

    # calculating cosines
    first_row_ids = sample_data.iloc[0].tf_idf

    results = []
    for _, row in sample_data.iterrows():
        res = cosine_similarity(first_row_ids, row.tf_idf)
        results.append(res)
    sample_data['cosine'] = results
    sample_data.sort_values(['cosine'], ascending=[False], inplace=True)
    print(sample_data.head())



def main():
    """ Entry point of the program"""
    print("Processing Starts")
    store = pd.HDFStore('store2.h5')
    df1 = store['df1']
    df2 = store['df2']
    gen_word_set(df1)
    # calculating term frequency
    count_freq_each_term_each_article(df1)

    # Question 1.1.1
    ger_wordset = df1[df1.name == "German"].iloc[0].word_set
    eu_wordset = df1[df1.name == "Europe"].iloc[0].word_set
    jacc_cof_eu_germany = calc_jaccard_similarity(eu_wordset, ger_wordset)
    print("Jaccard Coefficient in Document", jacc_cof_eu_germany)

    # Question 1.2
    # 1.2 Similarity of Graphs
    ger_outlink = df2[df2.name == "German"].iloc[0].out_links
    eu_outlink = df2[df2.name == "Europe"].iloc[0].out_links
    jacc_cof_eu_germany_links = calc_jaccard_similarity(set(ger_outlink), set(eu_outlink))
    print("Jaccard Coefficient in Links", jacc_cof_eu_germany_links)


    all_terms = set()
    for word_set in df1['word_set'].values:
        all_terms |= word_set

    all_docs = []
    for doc in df1['text']:
        all_docs.append(doc)

    doc_feq = Path('./doc_freq.txt')
    term_document_freq = None

    if doc_feq.is_file():
        with open('doc_freq.txt', 'r+') as f:
            term_document_freq = eval(f.read())
    else:
        term_document_freq = document_frequency_of_all_term(all_terms, all_docs)
        with open('doc_freq.txt', 'w+') as f:
            f.write(str(term_document_freq))

    # Calculate ifidf scores
    cal_tfidf_each_term(df1, term_document_freq)
    ger_tf_idf = df1[df1.name == "German"].iloc[0].tf_idf
    eu_tf_idf = df1[df1.name == "Europe"].iloc[0].tf_idf

    print("Cosine", calculate_cosine_similarity(ger_tf_idf, eu_tf_idf))
    compare_cosine_for_random_100_column(df1, calculate_cosine_similarity)



if __name__ == "__main__":
    main()
