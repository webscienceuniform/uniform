import math
import random
import numpy as np
import matplotlib.pyplot as plt

def gini_coefficient(tables, guests):
    """ calculates the gini coefficient"""
    length = len(tables)
    shared_table = dict()
    for table in tables:
        shared_table[table] = tables[table] / guests
    denom = 0
    for table in shared_table:
        denom += shared_table[table]
    denom = denom / length
    denom = 2 * denom
    temp = 0
    for i in shared_table:
        for j in shared_table:
            temp += abs(shared_table[i] - shared_table[j])
    temp = temp / math.pow(length, 2)
    gini_coe = temp / denom
    return gini_coe

def draw(list1, list2, list3, list4, list5):
    length = len(list1)
    x = length * [0]
    for i in range(length):
        x[i] = i + 1
    plt.xticks(np.arange(0,1001,100))
    plt.ylim(0,1)
    plt.title("Gini Coeficient")
    plt.xlabel("Subjects")
    plt.ylabel("Gini Coefficient")
    plt.plot(x, list1, label='Simulation 1',color="b")
    plt.plot(x, list2, label='Simulation 2',color="r")
    plt.plot(x, list3, label='Simulation 3',color="g")
    plt.plot(x, list4, label='Simulation 4',color="y")
    plt.plot(x, list5, label='Simulation 5',color="k")
    plt.legend(loc=0,fontsize='small')
    plt.show()

def sitting_at_table(customer_count):
    tables = dict()
    all_gini_coe = 1000 * [0]
    tables[1] = 1
    number_of_tables = 1
    number_of_all_guests = 1
    re = gini_coefficient(tables, number_of_all_guests)
    all_gini_coe[number_of_all_guests - 1] = re

    for i in range(2, customer_count + 1):
        number_of_all_guests += 1
        found = 0
        rand = random.random()
        for table in tables:
            prob = tables[table] / number_of_all_guests
            if rand < prob:
                tables[table] += 1
                found = 1
                re = gini_coefficient(tables, number_of_all_guests)
                all_gini_coe[number_of_all_guests - 1] = re
                break
        if found == 0:
            number_of_tables += 1
            tables[number_of_tables] = 1
            re = gini_coefficient(tables, number_of_all_guests)
            all_gini_coe[number_of_all_guests - 1] = re
    return all_gini_coe


def main():
    """ main """
    customers_num = 1000
    print("Simulating1... ")
    all_gini_coeff1 = sitting_at_table(customers_num)
    print("Simulating2... ")
    all_gini_coeff2 = sitting_at_table(customers_num)
    print("Simulating3... ")
    all_gini_coeff3 = sitting_at_table(customers_num)
    print("Simulating4... ")
    all_gini_coeff4 = sitting_at_table(customers_num)
    print("Simulating5... ")
    all_gini_coeff5 = sitting_at_table(customers_num)
    draw(all_gini_coeff1, all_gini_coeff2, all_gini_coeff3, all_gini_coeff4, all_gini_coeff5)


if __name__ == '__main__':
    main()



