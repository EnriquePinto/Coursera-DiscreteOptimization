#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def dynamic(input_data):
    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    # a trivial algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)
    
    m=np.zeros((capacity+1, item_count+1))
    for i in range(1,item_count+1):
        for k in range(1,capacity+1):
            if items[i-1].weight>k:
                m[k][i]=m[k][i-1]
            else:
                m[k][i]=max(m[k][i-1] , items[i-1].value+m[k-items[i-1].weight][i-1])   
    
    value = int(m[-1][-1])
    
    # traceback
    k=capacity
    for i in range(item_count,0,-1):
        if m[k][i]==m[k][i-1]:
            taken[i-1]=0
        else:
            taken[i-1]=1
            k=k-items[i-1].weight
            
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data   
