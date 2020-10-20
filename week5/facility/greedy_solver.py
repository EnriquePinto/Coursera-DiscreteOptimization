import sys
import os
from collections import namedtuple
import math
import matplotlib.pyplot as plt
from itertools import product
from random import sample, shuffle
import datetime
from tqdm import tqdm

Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def cost(solution, customers, facilities):
    # checks what was used
    used = []
    for i in solution:
        if i not in used:
            used.append(i)
    
    # calculate the cost of the solution
    obj = sum([facilities[f].setup_cost for f in used])
    
    for customer in customers:
        obj += length(customer.location, facilities[solution[customer.index]].location)
    
    return obj

def shuffle_list(*ls):
    l =list(zip(*ls))
    shuffle(l)
    return zip(*l)


def reorder(solution, customers, facilities):
    customer_count = len(customers)
    types = set(solution)
    types = list(types)
    groups = []
    for t in types:
        group = []
        for i in range(customer_count):
            if solution[i] == t:
                group.append(i)
        groups.append(group)
    return groups, types

def greedy_iter(c_order, customers, facilities):
    customer_count = len(customers)
    facility_count = len(facilities)
    # instantiate customer-facility assignment vector
    sol = [None] * customer_count
    
    # instantiate used facilities list
    used = []
    
    # instantiate available capacity vector
    av_cap = [None] * facility_count
    for f in facilities:
        av_cap[f.index] = f.capacity
    
    # go through greedy assignment
    for c in c_order:
        # checks for available facilities and stores their index
        av_facs = []
        for i in range(facility_count):
            if av_cap[i] >= customers[c].demand:
                av_facs.append(i)
        # checks available facilities for the one with smallest su_cost + distance
        # obs: if a facility is open, then its effective su_cost after being opened is 0
        best_cost = float('inf')
        best_idx = None
        for f in av_facs:
            if f in used:
                cost = length(customers[c].location,facilities[f].location)
            else:
                cost = (length(customers[c].location,facilities[f].location) +
                        facilities[f].setup_cost)
            # updates smallest cost found
            if cost < best_cost:
                best_cost = cost
                best_idx = f
        # updates solution assignment, used facilities and available capacity vector
        sol[c]=best_idx
        av_cap[best_idx] -= customers[c].demand
        #checks if facility is already open, if it isn't add it to list
        if best_idx not in used:
            used.append(best_idx)
    return sol
 
def cgreedy_solver(input_data):
    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])
    
    facilities = []
    for i in range(1, facility_count+1):
        parts = lines[i].split()
        facilities.append(Facility(i-1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3])) ))

    customers = []
    for i in range(facility_count+1, facility_count+1+customer_count):
        parts = lines[i].split()
        customers.append(Customer(i-1-facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))
    
    print('F count:',facility_count)
    print('C count:',customer_count)
    
    best_cost = float('inf')
    best_sol = None
    max_it = 1000
    
    # start with random order of clients
    c_order = sample(range(customer_count), customer_count)
    cost_hist = []
    best_cost_hist = []
    for i in tqdm(range(max_it)):
        solution = greedy_iter(c_order, customers, facilities)
        if cost(solution,customers, facilities) < best_cost:
            best_cost = cost(solution, customers, facilities)
            best_sol = solution
        # reorder
        cost_hist.append(cost(solution,customers, facilities))
        best_cost_hist.append(best_cost)
        #c_order = sorted(c_order,
         #                key = lambda x: length(customers[x].location,
          #                                      facilities[solution[x]].location)
           #                                      + facilities[solution[x]].setup_cost,
            #             reverse = False)
        # group by facilities 
        c_order = []
        groups, fac_g = reorder(solution, customers, facilities)
        groups, fac_g = shuffle_list(groups, fac_g)
        groups = list(groups)
        fac_g = list(fac_g)    
        for i in range(len(groups)):
            ordered_g =  sorted(groups[i], key = lambda x: length(customers[x].location,
                                                facilities[fac_g[i]].location)
                                                 + facilities[fac_g[i]].setup_cost,
                                 reverse = True)
            c_order.extend(ordered_g)
        
    solution = best_sol
    print(solution)
    
    
    
    print('Done iterating')
    # calculate the cost of the solution
    obj = cost(solution, customers, facilities)
    
    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))
    
    plt.subplot(1,2,1)
    sol_plot(input_data,solution)
    plt.subplot(1,2,2)
    plt.plot(cost_hist,'b')
    plt.plot(best_cost_hist,'r')
    return output_data