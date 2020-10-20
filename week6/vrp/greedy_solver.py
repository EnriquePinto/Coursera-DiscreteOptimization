import math
import numpy as np
from collections import namedtuple
from tqdm import tqdm
import sys
import os


Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])

def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)

def plot_data(customers,*args):
    for i in customers:
        if i.index!=0:
            plt.plot(i.x, i.y,'k.')
            plt.annotate(i.index,(i.x, i.y))
        else:
            plt.plot(i.x, i.y,'ro')
            plt.annotate('Dep.',(i.x, i.y))
    if args==None:
        return
    else:
        sol=args[0]
        cmap = plt.cm.rainbow
        c_idx=0
        for tour in sol:
            for i in range(len(tour)):
                plt.plot((customers[tour[i-1]].x, customers[tour[i]].x),
                 (customers[tour[i-1]].y, customers[tour[i]].y),'-',
                         color=cmap(c_idx/len(sol)))     
            c_idx+=1

            
def fits_capacity(v_tour,v_cap,customers):
    tot_demand=0
    for c in v_tour:
        tot_demand+=customers[c].demand
    if tot_demand<v_cap:
        return True
    else:
        return False

def tour_cost(v_tour,customers):
    cost=0
    for i in range(len(v_tour)):
        cost+=length(customers[v_tour[i-1]],customers[v_tour[i]])
    return cost

def tour_demand(v_tour,customers):
    dem=0
    for i in v_tour:
        dem+=customers[i].demand
    return dem

def objec(tours,customers):
    obj=0
    for t in tours:
        obj+=tour_cost(t,customers)
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

def two_opt_search(tour,customers):
    nodeCount=len(tour)
    best_tour=tour
    best_obj=tour_cost(tour,customers)
    for i in range(1,nodeCount-1):
            for j in range(1,nodeCount-1):
                p_tour=idx_two_opt(best_tour,i,j)
                p_obj=tour_cost(p_tour,customers)
                if p_obj<best_obj:
                    best_tour=p_tour
                    best_obj=p_obj
    return best_tour


def vr_solver(input_data):
    # Currently returns infeasible solutions for some problems!

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    customer_count = int(parts[0])
    vehicle_count = int(parts[1])
    vehicle_capacity = int(parts[2])
    
    print('Customer Count:',customer_count)
    print('Vehicle Count',vehicle_count)
    print('Vehicle Cap.',vehicle_capacity)
    
    customers = []
    for i in range(1, customer_count+1):
        line = lines[i]
        parts = line.split()
        customers.append(Customer(i-1, int(parts[0]), float(parts[1]), float(parts[2])))

    #the depot is always the first customer in the input
    depot = customers[0] 

    # greedy solution
    # assign customers to vehicles sorted by a balance (alpha) of distance and demand

    
    obj_hist = []
    
    best_obj = float('Inf')
    best_tours = []
    
    alpha_n=100
    # Iterate in a range alpha taking the best!
    for alpha in tqdm(np.linspace(0,1,alpha_n)):
        vehicle_tours = []
        remaining_customers = set(customers)
        remaining_customers.remove(depot)
        for v in range(0, vehicle_count):
            # print "Start Vehicle: ",v
            vehicle_tours.append([])
            capacity_remaining = vehicle_capacity
            current_c=0
            full=False
            while len(remaining_customers)>0 and not full:
                sorted_rem_cust=sorted(remaining_customers,
                                        key=lambda x: alpha*(length(customers[current_c],x)) + 
                                       (1-alpha)*(-x.demand), reverse = False)
                for c in sorted_rem_cust:
                    if c.demand<=capacity_remaining:
                        capacity_remaining-=c.demand
                        remaining_customers.remove(c)
                        current_c=c.index
                        vehicle_tours[v].append(c.index)
                        break
                #check if vehicle is effectively full!!
                full=True
                for c in remaining_customers:
                    if c.demand<=capacity_remaining:
                        full=False
                        break
        # checks that the number of customers served is correct
        valid = False
        if sum([len(v) for v in vehicle_tours]) == len(customers) - 1:
            valid=True
        # IDEA: RUN TRAVELING SALESMAN FOR EACH VALID TOUR
        # calculates objective for valid tour
        if valid == True:
            # the formulation pressuposes '0' at the start and end of tour
            # adding '0' to start and end
            for t in vehicle_tours:
                t.insert(0,0)
                t.append(0)
            # calculate the cost of the solution; for each vehicle the length of the route
            obj=objec(vehicle_tours,customers)
            if obj<best_obj:
                best_obj=obj
                best_tours = vehicle_tours
                obj_hist.append(obj)
            else:
                obj_hist.append(obj)
        else:
            obj_hist.append(None)
    
    
    vehicle_tours=best_tours
    
    for i in range(len(vehicle_tours)):
        vehicle_tours[i]=two_opt_search(vehicle_tours[i],customers)

    # calculate the cost of the solution; for each vehicle the length of the route
    obj=objec(vehicle_tours,customers)
    print('Cost:',obj)

    # prepare the solution in the specified output format
    outputData = '%.2f' % obj + ' ' + str(0) + '\n'
    for v in range(0, vehicle_count):
        outputData += ' '.join([str(customers[c].index) for c in vehicle_tours[v]]) + '\n'

    return outputData
