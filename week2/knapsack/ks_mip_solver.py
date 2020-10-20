#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from solver_greedy import greedy
from collections import namedtuple
from mip import Model, xsum, maximize, OptimizationStatus, VarList, SearchEmphasis
import datetime
Item = namedtuple("Item", ['index', 'value', 'weight'])

def mip_solver(input_data):
    # Modify this code to run your optimization algorithm

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
    
    # declare value vector
    val_vec = [item.value for item in items]
    
    # declare weight vector scaled by capacity
    wgt_vec = [item.weight/capacity for item in items]
    
    # start MIP solver
    m = Model(solver_name='GRB')
    print('-Model instatiated!',datetime.datetime.now())
    
    # states search emphasis
    #     - '0' (default) balanced approach
    #     - '1' (feasibility) aggressively searches for feasible solutions
    #     - '2' (optimality) explores search space to tighten dual gap
    m.emphasis = 2
    
    # whenever the distance of the lower and upper bounds is less or 
    # equal max_gap*100%, the search can be finished
    m.max_gap = 0.05
    
    # specifies number of used threads
    # 0 uses solver default configuration, 
    # -1 uses the number of available processing cores 
    # ≥1 uses the specified number of threads. 
    # An increased number of threads may improve the solution time but also increases 
    # the memory consumption. Each thread needs to store a different model instance!
    m.threads = -1
    
    
    # controls the generation of cutting planes
    # cutting planes usually improve the LP relaxation bound but also make the solution time of the LP relaxation larger
    # -1 means automatic
    #  0 disables completely
    #  1 (default) generates cutting planes in a moderate way
    #  2 generates cutting planes aggressively
    #  3 generates even more cutting planes
    m.cuts=-1

    m.preprocess=1
    m.pump_passes=10
    m.sol_pool_size=1
    
    # instantiates taken items variable vector
    taken = [m.add_var(name="it{}".format(i),var_type='B') for i in range(item_count)]
    print('-Variables declared!',datetime.datetime.now())
    
    # instantiates objective function
    m.objective = maximize( xsum( val_vec[i]*taken[i] for i in range(item_count) ) )
    print('-Objective declared!',datetime.datetime.now())
    
    m.add_constr( xsum( wgt_vec[i]*taken[i] for i in range(item_count)) <=1 )
    print('-Contraints processed!',datetime.datetime.now())
    
    #Maximum time in seconds that the search can go on if a feasible solution 
    #is available and it is not being improved
    mssi = 1000 #default = inf
    # specifies maximum number of nodes to be explored in the search tree (default = inf)
    mn = 40000 #default = 1073741824
    # optimize model m within a processing time limit of 'ms' seconds
    ms = 3000 #default = inf
    
    print('-Optimizer start.',datetime.datetime.now())
    # executes the optimization
    #status = m.optimize(max_seconds = ms,max_seconds_same_incumbent = mssi,max_nodes = mn)
    status = m.optimize(max_seconds = ms , max_seconds_same_incumbent = mssi)
    final_obj = m.objective_value
    
    print('Opt. Status:',status)
    print('MIP Sol. Obj.:',final_obj)
    print('Dual Bound:',m.objective_bound)
    print('Dual gap:',m.gap)
    
    sol = [round(it.x) for it in taken]
    value = int(final_obj)
    
    taken = sol
    # prepare the solution in the specified output format
    if status == OptimizationStatus.OPTIMAL:
        output_data = str(value) + ' ' + str(1) + '\n'
        output_data += ' '.join(map(str, taken))
    elif status == OptimizationStatus.FEASIBLE:
        output_data = str(value) + ' ' + str(0) + '\n'
        output_data += ' '.join(map(str, taken))


    if item_count == 10000:
        output_data=greedy(input_data)

    return output_data
