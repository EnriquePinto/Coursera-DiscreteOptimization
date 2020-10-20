#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import math
from typing import List, Tuple
from collections import namedtuple
import matplotlib.pyplot as plt
import random
from tqdm import tqdm
from itertools import product
import datetime

plt.rcParams['figure.figsize'] = [18, 13]

Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
        
def objec(solution,points,d_m):
    nodeCount=len(points)
    obj = d_m[solution[-1]][solution[0]]
    for index in range(0, nodeCount-1):
        obj += d_m[solution[index]][solution[index+1]]
    return obj

def idx_two_opt(sol, idx1, idx2):
    # makes the reversal 
    if idx1<idx2:
        sol1=sol[:idx1]
        sol2=list(reversed(sol[idx1:idx2+1]))
        sol3=sol[idx2+1:]
    else:
        sol1=sol[:idx2]
        sol2=list(reversed(sol[idx2:idx1+1]))
        sol3=sol[idx1+1:]
    new_sol=sol1+sol2+sol3
    return new_sol
        
def two_opt_search(sol,points,d_m):
    nodeCount=len(points)
    best_sol=sol
    best_obj=objec(sol,points,d_m)
    for i in tqdm(range(nodeCount)):
            for j in range(nodeCount):
                p_sol=idx_two_opt(best_sol,i,j)
                p_obj=objec(p_sol,points,d_m)
                if p_obj<best_obj:
                    best_sol=p_sol
                    best_obj=p_obj
    return best_sol

def twoopt_solver(input_data):
    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))
    print('Points parsed!')
    
    # calculate distance matrix
    d_m = [ [length(q,p) for q in points] for p in points]
    print('Distance matrix ready!')

    S=[i for i in range(nodeCount)]
    n_it = 5
    thld = 1
    obj = objec(S,points,d_m)

    for i in range(n_it):
        print('Two opt it ({}/{})'.format(i+1,n_it))
        s_obj = obj
        S = two_opt_search(S,points,d_m)
        obj=objec(S,points,d_m)
        print('S obj = {} / F obj = {}'.format(s_obj,obj))
        if obj/s_obj >= thld:
            print('No significant improvement, breaking.')
            break

    obj=objec(S,points,d_m)

    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, S))

    return output_data