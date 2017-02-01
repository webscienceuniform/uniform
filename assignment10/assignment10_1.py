from collections import Counter
from math import log2
import time
import operator
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def is_valid_date(date_str):
    """ returns True iff givin date is valid"""
    try:
        valid_date = time.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return False
    else:
        return True

def draw_plot(user_entropy, system_entropy):
    i = 0
    x = len(user_entropy) * [0]
    while i < len(x):
        x[i] = i+1
        i += 1
    print(x)
    plt.xticks(np.arange(0, max(x), 40))
    plt.yticks(range(0,int(max(system_entropy) + 2)))
    plt.title("Sorted System Entropy and user Entropy (Average) per day")
    plt.xlabel("Days Rank (base on Entropy)")
    plt.ylabel("Entropy")
    plt.scatter(x, user_entropy, label='User Entropy', color="r")
    plt.scatter(x, system_entropy, label='System Entropy', color="b")
    plt.legend(loc=2)
    plt.show()

def info_according_to_date(date, datas):
    dic = dict()
    dic['date'] = date
    dic['tweets'] = Counter()
    dic['names'] = dict()
    for data in datas:
        if data[1] == date:
            name = data[0]
            tweet = data[2]
            if name not in dic['names']:
                dic['names'][name] = Counter(tweet.split(" "))
            else:
                dic['names'][name] += Counter(tweet.split(" "))
            dic['tweets'] += Counter(tweet.split(" "))
    return dic


def cal_entropy(arr_twee_num):
    entropy = 0.0
    total = sum(arr_twee_num)
    for val in arr_twee_num:
        prob =  val / total
        entropy = entropy + prob * log2(prob)
    return abs(entropy)

def extract_counter(conter):
    count_values = []
    for _, val in dict(conter).items():
        count_values.append(val)
    return count_values

def cal_user_entropy(user_info):
    return cal_entropy(extract_counter(user_info))


def cal_sys_entropy(tweets_info):
    return cal_entropy(extract_counter(tweets_info))

def main():
    """ entry point of the application"""
    system_entropies = []
    average_entropies = []

    df = pd.read_csv("onlyhash.data", sep="\t", header = None)
    df.columns = ["user", "date", "#tag"]
    df.groupby('date').head()
    df = df[df['date'].map(is_valid_date) != False]
    unique_dates = df['date'].unique()
    for date in unique_dates:
        print(" Processing ", date)
        raw_data = df[df['date'] == date]
        all_data = raw_data.values.tolist()
        info = info_according_to_date(date, all_data)
        tweets = info['tweets']
        names = info['names']
        user_entropies = []

        for name, info_user in names.items():
            user_entropies.append(cal_user_entropy(info_user))
        sum_of = sum(user_entropies)
        try:
            average_entropy = sum_of / len(user_entropies)
        except Exception:
            print("Died on ",  date)
            average_entropy = 0

        average_entropies.append(average_entropy)
        system_entropies.append(cal_user_entropy(tweets))

    # lets sort it
    average_entropies = sorted(average_entropies)
    system_entropies = sorted(system_entropies)
    draw_plot(average_entropies, system_entropies)

if __name__ == '__main__':
    main()
