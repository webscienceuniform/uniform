# pylint: disable=C0103
# -*- coding: utf-8 -*-
""" Assignment for Web Science
  Group:  uniform
  Members:
    - Jalak Arvind Kumar Pansuriya (jalakpansuriya@uni-koblenz.de)
    - Madhu Rakhal Magar (rakhalmadhu@uni-koblenz.de)
    - Pradip Giri (pradipgiri@uni-koblenz.de)
"""
import random
import math
import matplotlib.pyplot as plt


def apply_math_func(math_func, arrary_of_number):
    """ return new list containing math values after applying given math
    function."""
    return [math_func(x) for x in arrary_of_number]

# generating random 10 numbers
random_numbers = random.sample(range(0, 90), 10)

# Performing sin on each random number
SIN = apply_math_func(math.sin, random_numbers)

# Performing cos on each random number
COSIN = apply_math_func(math.cos, random_numbers)

# Plotting the graph
plt.plot(SIN, color="red", label="Sine")
plt.plot(COSIN, color="blue", label="Cosine")
plt.title('Sine and Cosine of 10 random values')
plt.xlabel('X axis ')
plt.ylabel('Y axis')
plt.legend(loc='upper right')
plt.legend(shadow=True, fancybox=True)
plt.show()
