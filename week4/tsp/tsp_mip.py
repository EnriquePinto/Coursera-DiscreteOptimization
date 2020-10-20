#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import math
from collections import namedtuple
import random
from tqdm import tqdm
from itertools import product
from mip import Model, xsum, minimize, OptimizationStatus, VarList, SearchEmphasis
import datetime

Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def tsp_mip_solver(input_data):
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
    
    # declare MIP model
    m = Model(solver_name='GRB')
    print('-Model instatiated!',datetime.datetime.now())
    
    # states search emphasis
    #     - '0' (default) balanced approach
    #     - '1' (feasibility) aggressively searches for feasible solutions
    #     - '2' (optimality) explores search space to tighten dual gap
    m.emphasis = 0
    
    # whenever the distance of the lower and upper bounds is less or 
    # equal max_gap*100%, the search can be finished
    m.max_gap = 0.05
    
    # specifies number of used threads
    # 0 uses solver default configuration, 
    # -1 uses the number of available processing cores 
    # ≥1 uses the specified number of threads. 
    # An increased number of threads may improve the solution time but also increases 
    # the memory consumption. Each thread needs to store a different model instance!
    m.threads = 0
    
    
    # controls the generation of cutting planes
    # cutting planes usually improve the LP relaxation bound but also make the solution time of the LP relaxation larger
    # -1 means automatic
    #  0 disables completely
    #  1 (default) generates cutting planes in a moderate way
    #  2 generates cutting planes aggressively
    #  3 generates even more cutting planes
    m.cuts=-1

    m.preprocess=1
    m.pump_passes=20
    m.sol_pool_size=1
    
    nodes = set(range(nodeCount))
    
    # instantiate "entering and leaving" variables
    x = [ [m.add_var(name="x{}_{}".format(p,q),var_type='B') for q in nodes] for p in nodes ] 
    # instantiate subtour elimination variables 
    y = [ m.add_var(name="y{}".format(i)) for i in nodes ]
    print('-Variables instantiated',datetime.datetime.now())
    
    # declare objective function
    m.objective = minimize( xsum( d_m[i][j]*x[i][j] for i in nodes for j in nodes) )
    
    print('-Objective declared!',datetime.datetime.now())
    
    # declare constraints
    # leave each city only once
    for i in tqdm(nodes):
        m.add_constr( xsum(x[i][j] for j in nodes - {i}) == 1 )

    # enter each city only once
    for i in tqdm(nodes):
        m.add_constr( xsum(x[j][i] for j in nodes - {i}) == 1 )
    
    # subtour elimination constraints
    for (i, j) in tqdm(product(nodes - {0}, nodes - {0})):
        if i != j:
            m.add_constr( y[i] - (nodeCount+1)*x[i][j] >= y[j]-nodeCount )
            
    print('-Constraints declared!',datetime.datetime.now())
    
    #Maximum time in seconds that the search can go on if a feasible solution 
    #is available and it is not being improved
    mssi = 1000 #default = inf
    # specifies maximum number of nodes to be explored in the search tree (default = inf)
    mn = 1000000 #default = 1073741824
    # optimize model m within a processing time limit of 'ms' seconds
    ms = 3000 #default = inf
    
    # executes the optimization
    print('-Optimizer start.',datetime.datetime.now())
    #status = m.optimize(max_seconds = ms,max_seconds_same_incumbent = mssi,max_nodes = mn)
    status = m.optimize(max_seconds = ms , max_seconds_same_incumbent = mssi)

    print('Opt. Status:',status)
    print('MIP Sol. Obj.:',m.objective_value)
    print('Dual Bound:',m.objective_bound)
    print('Dual gap:',m.gap)
    
    sol= [0]
    c_node=0
    for j in range(nodeCount-1):
        for i in range(nodeCount):
            if round(m.var_by_name("x{}_{}".format(c_node,i)).x) != 0:
                sol.append(i)
                c_node=i
                break
    
    obj=m.objective_value
    
    # prepare the solution in the specified output format
    if status == OptimizationStatus.OPTIMAL:
        output_data = '%.2f' % obj + ' ' + str(1) + '\n'
        output_data += ' '.join(map(str, sol))
    elif status == OptimizationStatus.FEASIBLE:
        output_data = '%.2f' % obj + ' ' + str(0) + '\n'
        output_data += ' '.join(map(str, sol))

    return output_data