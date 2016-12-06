import os
import sys
import glob
import numpy as np
import matplotlib.pyplot as plt


path = os.getcwd() + '/' + 'foreign-words'
article_file = os.getcwd() + '/' + 'simple-20160801-1-article-per-line'
all_foreign_words = set([])

# this is list wich will contain number of foreign words
artile_infos_with_foreign_words = []

def open_file(file_name):
    file_content = None
    with open(file_name, 'r+') as f:
        file_content = f.read()
    return file_content

def process_foreign_text_file(file_name):
    file_content = open_file(file_name)
    list_of_words = eval(file_content)
    for word in list_of_words:
        all_foreign_words.add(word.strip())

def process_articles(articles):
    all_articles = articles.split('\n')
    for id, article in enumerate(all_articles):
        words_arr = article.split(" ")
        #article having less than 15 words are discarded
        if len(words_arr) > 15:
            found_world = 0
            for word in words_arr:
                if word.strip() in all_foreign_words:
                    found_world += 1
            artile_infos_with_foreign_words.append({"id": id, "loan_word": found_world, "total_word": len(words_arr)})

def mean(arr):
    return np.mean(arr)

def median(arr):
    return np.median(arr)


def plot_graph(data):
    num_bins = 100
    counts, bin_edges = np.histogram(data, bins=num_bins, normed=True)
    cdf = np.cumsum(counts)
    plt.plot(bin_edges[1:], cdf)
    plt.xlabel('Article')
    plt.ylabel('Loaned World %')
    plt.show()


def main():
    all_txt_files = glob.glob(path + '/*.txt')
    for text_file in all_txt_files:
        process_foreign_text_file(text_file)
    artile_content = open_file(article_file)
    process_articles(artile_content)
    with open("result.txt", "w+") as f:
        sorted_list = sorted(artile_infos_with_foreign_words, key=lambda info: info['loan_word'])
        f.write(str(sorted_list))
    arr = list(map(lambda x: (x['total_word'], x['loan_word']), artile_infos_with_foreign_words))
    plot_graph(arr)
    arr = list(map(lambda x: x[1], arr))
    print("median", median(arr))
    print("mean", mean(arr))
    print("unique loaned word used ", len(all_foreign_words))


def draw_scatter_plot(arr):
    total_word = [x[0] for x in arr]
    foreign_word = [x[1] for x in arr]
    N = len(total_word)
    colors = np.random.rand(N)
    plt.scatter(total_word, foreign_word, s=15, c=colors, alpha=1)
    plt.ylabel('Loaned Word')
    plt.xlabel('Total Words')
    plt.xlim(0, 10000)
    plt.ylim(0, 1500)
    plt.show()

def process_diagram():
    raw_data = None
    with open("result.txt", "r+") as f:
        raw_data = eval(f.read())
    if raw_data:
        arr = list(map(lambda x: (x['total_word'], x['loan_word']), raw_data))
        plot_graph(arr)
        draw_scatter_plot(arr)

if __name__ == "__main__":
    plot = None
    try:
        plot = sys.argv[1]
    except:
        pass
    if plot == "plot":
        process_diagram()
    else:
        main()
