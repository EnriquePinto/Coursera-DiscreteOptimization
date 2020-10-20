#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

from solver_greedy import greedy
from solver_dynamic import dynamic

def mixed(input_data):
    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])
    
    # if data is small enough, solve with dynamic programming
    if (item_count*capacity)<=(500*50000):
        output_data=dynamic(input_data)
    #else, try greedy
    else:
        output_data=greedy(input_data)
    return output_data 
