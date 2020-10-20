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

def greedy_solve(points,s_node,k_nn):
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
        # first choose k_nn and check availability
        found=0
        # go through k_nn starting closest to c_node and check if available
        for i in k_nn[c_node]:
            if i in av_nodes:
                found=1
                next_node=i
                break
            else:
                next_node = min(av_nodes,key=lambda x:length(points[c_node],points[x]))
        # update current node        
        c_node=next_node
        vis_list.append(c_node) 
    solution = vis_list
    return solution

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
        plt.plot(i.x, i.y,'rx')
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
        sol[idx1:idx2+1]=list(reversed(sol[idx1:idx2+1]))
    else:
        sol[idx2:idx1+1]=list(reversed(sol[idx2:idx1+1]))

    return sol
  
def compute_k_neighbors(k,points):
    nodeCount=len(points)
    k_nn=[]
    if(k>nodeCount):
        k=nodeCount
    for i in tqdm(range(nodeCount)):
        nn=sorted(range(nodeCount),key=lambda x:length(points[i],points[x]))
        nn=nn[1:k+1]
        k_nn.append(nn)
    return k_nn
    
def sim_anneal(s0,points,k_nn,T0=60,alpha=0.9995,maxit=30000, m_length=1, stop_thld=1000):
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
    
    stop_clk=0
    
    for i in range(maxit):       
        obj_hist.append(obj)
        T_hist.append(T)       
        p_s=s
        
        # 2OPT NEIGHBORHOOD STEP
        # get two random nodes 
        n1=random.randrange(nodeCount)
        n2=random.choice(k_nn[n1])

        p_s=two_opt(p_s,n1,n2) 
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
            stop_clk=0
        else:
            stop_clk=stop_clk+1
            
        # stop if no improvement is made 
        if stop_clk>=stop_thld:
            break
        
        T=T*alpha
    return s,best_s, a_prob_hist, obj_hist, T_hist

def sim_anneal_tqdm(s0,points,T0=60,alpha=0.9995,maxit=30000, m_length=1, stop_thld=1000):
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
    
    stop_clk=0
    
    for i in tqdm(range(maxit)):       
        obj_hist.append(obj)
        T_hist.append(T)       
        p_s=s
        
        # 2OPT NEIGHBORHOOD STEP
        # get two random nodes 
        n1=random.randrange(nodeCount)
        if n1+300<nodeCount:
        	n2=random.choice(range(n1,n1+1000))
        else:
        	n2=random.choice(range(n1-1000,n1))
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
            stop_clk=0
        else:
            stop_clk=stop_clk+1
            
        # stop if no improvement is made 
        if stop_clk>=stop_thld:
            break
        
        T=T*alpha
    return s,best_s, a_prob_hist, obj_hist, T_hist

def new_annealing_solver(input_data,greedy=False,k=1000):
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
    
    #compute k nearest neighbors
    k_nn=compute_k_neighbors(k,points)
    print('Neighbor matrix ready!')
    
    if greedy==True:
        # gets random greedy solution
        starting_node=random.randint(0,nodeCount)
        solution=greedy_solve(points,starting_node,k_nn)
        print('Greedy Ready!')
        s0=solution      
    else:
        s0=random.sample(range(nodeCount), nodeCount)

    greedy_sol=s0
    # find an improved solution with simulated annealing 2-opt neighborhood

    
    # NOTE1: Relate temperature with edge_length (Uncertain, perhaps unnecessary)
    # NOTE2: Try doing grid searched annealing runs and get the best (TOO EXPENSIVE ON THE FLY)
    # NOTE3: Include swaps in the neighborhood (WORSE THAN 2OPT)
    # NOTE4: Keep track of best solution and break if it doesn't improve for a while,
    #        afterwards do new SA run with different parameters. (May be surpassed by good sched.)
    # NOTE5: Use cached k-nearest neighbors instead of full nearest neighbors
    # NOTE6: Implement 2-OPT Heuristic and check runtime (BAD)
    # NOTE7: Keep list of k-nearest neighbors, in SA: 1.select random node, 2. select random
    #        node from nearest neighbor list, 3. perform 2opt swap and submit    
    
    sa_maxit=40
    a_prob_hist=[]
    obj_hist=[]
    T_hist=[]
    #T0=100
    best_ever_s=s0
    best_s=s0
    s=s0
    obj_clk=0
    best_thld=2
    if nodeCount<900:
    	if nodeCount<300:
    		if nodeCount<=100:
    			stop_thld=50000
    			sa_maxit=400
    			best_thld=3
    		else:
    			stop_thld=40000
    			sa_maxit=300
    			best_thld=3
    	else:
    		stop_thld=20000
    		sa_maxit=400
    		best_thld=3
    else:
    	if nodeCount>20000:
    		stop_thld=40000
    		sa_maxit=1
    		best_thld=1
    	else:
    		stop_thld=40000 
    		sa_maxit=15
    		best_thld=1
    T0=max([objec(s0,points)/nodeCount, 15])

    for i in range(sa_maxit):
        #print('T0:',T0,' Current Best:',objec(best_ever_s,points),'Starting State Obj:',objec(s,points), i, '/', sa_maxit )
        print('T0: %.2f | Best: %.2f | Starting obj: %.2f | it %d/%d' 
              %(T0, objec(best_ever_s,points), objec(s,points), i+1, sa_maxit ) )
        if nodeCount<20000:
        	s, best_s, a_p_hist, o_hist, T1_hist = sim_anneal(s,points,k_nn,T0,alpha=0.9999,
                                                  maxit=100000,stop_thld=stop_thld)
        else:
        	s, best_s, a_p_hist, o_hist, T1_hist = sim_anneal_tqdm(s,points,T0,alpha=0.9999,
                                                  maxit=50000,stop_thld=stop_thld)
        a_prob_hist.extend(a_p_hist)
        obj_hist.extend(o_hist)
        T_hist.extend(T1_hist)        
        #T0=objec(s,points)/nodeCount
        T0=T0*0.4

        if objec(best_s,points)<objec(best_ever_s,points):
            best_ever_s=best_s
            obj_clk=0
            #checks if obj is good enough:
            if nodeCount==51 and objec(best_ever_s,points)<430:
            	break
            elif nodeCount==100 and objec(best_ever_s,points)<20800:
            	break
            elif nodeCount==200 and objec(best_ever_s,points)<30000:
            	break
            elif nodeCount==574 and objec(best_ever_s,points)<37600:
            	break
            elif nodeCount==1889 and objec(best_ever_s,points)<323000:
            	break
            elif nodeCount==33810 and objec(best_ever_s,points)<78478868:
            	break
        else:
        	obj_clk=obj_clk+1

        if obj_clk>=best_thld:
        	s=best_ever_s
        	obj_clk=0
        	T0=max([objec(s0,points)/nodeCount, 15])
        	print('>Node Reset<')   	

        #Checks if satisfies course requirements

    # Do a cooling full run
    #print('Cooling Run, Starting obj.= %.2f' %objec(best_ever_s,points))
    #T0=max([objec(s0,points)/nodeCount, 50])
    #ph1, last_r, ph2, ph3, ph4=sim_anneal(best_ever_s,points,k_nn,T0,alpha=0.999,
    #                                              maxit=200000,stop_thld=40000)
    
    #if objec(last_r,points)<objec(best_ever_s,points):
    #    best_ever_s=last_r
    #    print('Cooling improved solution!')


    print('Start Obj:',objec(s0,points))
    print('End Obj:',objec(best_ever_s,points))
    print('Delta Obj:',objec(s0,points)-objec(best_ever_s,points))
    
    
    obj=objec(best_ever_s,points)
    solution=best_ever_s
    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

