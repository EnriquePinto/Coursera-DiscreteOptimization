#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import math
from collections import namedtuple
import matplotlib.pyplot as plt
import random
from tqdm import tqdm

Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def objec(solution,points):
    nodeCount=len(points)
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount-1):
        obj += length(points[solution[index]], points[solution[index+1]])
    return obj

def greedy_solve(points,s_node,d_m):
    nodeCount=len(points)
    # visit the unvisited node that is closest to current node
    vis_list=[]
    # starts on random node
    #c_node=random.randint(0,nodeCount-1)
    c_node=s_node
    vis_list.append(c_node)
    for i in tqdm(range(nodeCount-1)):     
        #checks available nodes
        av_nodes = [n for n in list(range(0,nodeCount)) if n not in vis_list]
        next_node = closest_av_node(c_node,av_nodes,d_m)
        c_node=next_node
        vis_list.append(c_node) 
    solution = vis_list
    return solution

def closest_av_node(c_node,av_nodes,d_m):
    d_list=d_m[c_node]
    clos_dist=d_list[av_nodes[0]]
    clos_n=av_nodes[0]
    for n in av_nodes:
        if d_list[n]<clos_dist and d_list[n]!=0:
            clos_n=n
            clos_dist=d_list[n]
    return clos_n

def sol_plot(solution,points):
    nodeCount=len(points)
    # plot the solution
    j=0
    for i in points:
        plt.plot(i.x, i.y,'ko')
        #plt.annotate(j,(i.x, i.y))
        j=j+1
    
    for i in range(-1, nodeCount-1):
        plt.plot((points[solution[i]].x, points[solution[i+1]].x),
                 (points[solution[i]].y, points[solution[i+1]].y),'-')
    
def data_plot(points):
    nodeCount=len(points)
    # plot the solution
    j=0
    for i in points:
        plt.plot(i.x, i.y,'ko')
        #plt.annotate(j,(i.x, i.y))
        j=j+1

def two_opt(sol, node1, node2):
    # finds the position of desired nodes in solution list
    idx1=sol.index(node1)
    idx2=sol.index(node2)
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

def swap(sol, idx1, idx2):
    out_sol=sol
    val1=sol[idx1]
    val2=sol[idx2]
    out_sol[idx1]=val2
    out_sol[idx2]=val1
    return out_sol


def sim_anneal(s0,points,T0=60,alpha=0.9995,maxit=30000, m_length=1):
    s=s0
    T=T0
    nodeCount=len(points)    
    #calculate objective of solution
    obj=objec(s,points)
    
    best_obj=obj
    best_s=s
    
    a_prob_hist=[]
    obj_hist=[]
    T_hist=[]
    
    for i in range(maxit):       
        obj_hist.append(obj)
        T_hist.append(T)       
        p_s=s
        
        # 2OPT NEIGHBORHOOD STEP
        # get two random nodes 
        n1,n2=random.sample(range(nodeCount), 2)
        p_s=idx_two_opt(p_s,n1,n2) 
        p_obj=objec(p_s,points)
        # calculates acceptance probability
        if p_obj<obj:
            a_prob=1
        else:
            a_prob=math.exp(-(p_obj-obj)/T)
        a_prob_hist.append(a_prob)
        # ROLL THE DICE!
        if a_prob>random.uniform(0, 1):
            s=p_s
            #alpha=p_obj/obj
            obj=p_obj
        # saves best solution    
        if obj<best_obj:
            best_s=s
            best_obj=obj
        
        T=T*alpha
    return best_s, a_prob_hist, obj_hist, T_hist

def annealing_solver(input_data,greedy=False):
    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])
    print('Node Count:',nodeCount)

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))
    print('Points Parsed!')
    
    if greedy==True:
        # gets distance matrix
        d_m=[]
        for i in tqdm(range(nodeCount)):
            d_i=[]
            for j in range(nodeCount):
                d_i.append(length(points[i],points[j]))
            d_m.append(d_i)  
        
        print('Distance Matrix Ready')
    
        # gets random greedy solution
        solution=greedy_solve(points,random.randint(0,nodeCount),d_m)
        print('Greedy Ready!')
        s0=solution
        
    else:
        s0=random.sample(range(nodeCount), nodeCount)

    
    # find an improved solution with simulated annealing 2-opt neighborhood

    
    # NOTE1: Relate temperature with edge_length (Uncertain, perhaps unnecessary)
    # NOTE2: Try doing grid searched annealing runs and get the best (TOO EXPENSIVE ON THE FLY)
    # NOTE3: Include swaps in the neighborhood (WORSE THAN 2OPT)
    # NOTE4: Keep track of best solution and break if it doesn't improve for a while,
    #        afterwards do new SA run with different parameters. (May be surpassed by good sched.)
    # NOTE5: Use cached k-nearest neighbors instead of full nearest neighbors
    # NOTE6: Implement 2-OPT Heuristic and check runtime
    
    sa_maxit=50
    a_prob_hist=[]
    obj_hist=[]
    T_hist=[]
    T0=100
    best_s=s0
    start_s=s0
    for i in tqdm(range(sa_maxit)):
        s, a_p_hist, o_hist, T1_hist = sim_anneal(s0,points,T0,alpha=0.995,maxit=5000)
        s0=s
        a_prob_hist.extend(a_p_hist)
        obj_hist.extend(o_hist)
        T_hist.extend(T1_hist)
        #T0=10*T1_hist[-1]
        T0=T0*0.9
        if objec(s,points)<objec(best_s,points):
            best_s=s

    print('Start Obj:',objec(start_s,points))
    print('End Obj:',objec(s,points))
    print('Delta Obj:',objec(start_s,points)-objec(s,points))
    # plot solution
    #plt.subplot(2,2,1)
    #plt.semilogy(T_hist)
    #plt.grid(1)
    
    #plt.subplot(2,2,2)
    #sol_plot(s,points)
    
    #plt.subplot(2,2,3)
    #plt.plot(a_prob_hist,'.')
    
    #plt.subplot(2,2,4)
    #plt.plot(obj_hist)
    #plt.grid(1)
    #plt.show()

    obj=objec(s,points)
    solution=s
    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data