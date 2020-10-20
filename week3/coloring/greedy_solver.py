import numpy as np
from collections import Counter, OrderedDict
from math import floor,ceil
from tqdm import tqdm
import sys  
import os

def maxelements(seq):
    ''' Return list of position(s) of largest element '''
    max_indices = []
    if seq:
        max_val = seq[0]
        for i,val in ((i,val) for i,val in enumerate(seq) if val >= max_val):
            if val == max_val:
                max_indices.append(i)
            else:
                max_val = val
                max_indices = [i]

    return max_indices

def avail_color(color_list):
    i=0
    while True:
        if i not in color_list:
            return i
        i += 1
        
def greedy(neigh_nds,nd_order):
    color = dict()
    for nd in nd_order:
        used_neighbour_colors = [color[nbr] for nbr in neigh_nds[nd]
                                 if nbr in color]
        color[nd] = avail_color(used_neighbour_colors)
    return color

def color_sort(sol):
    chr_nbr=max(sol)+1
    #sort by color and degrees
    order=[]
    for i in range(chr_nbr):
        c_list=[]
        for j in range(len(sol)):
            if sol[j]==i:
                c_list.append(j)
        order.append(c_list)
    return order

def it_greedy_solver(input_data,maxit):
    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    #defines list of neighbor nodes
    neigh_nds=[]
    for i in range(node_count):
        neigh_nds_t=[]
        for k in range(edge_count):
            if (i in edges[k]):
                idx=edges[k].index(i)
                neigh_nds_t.append(edges[k][(idx-1)])
        neigh_nds.append(neigh_nds_t)   
    
    nd_lgth=[]
    for n in neigh_nds:
        nd_lgth.append(len(n))
    
    
    #nodes sorted by number of neighbors: (nd, #of nghbrs)
    sorted_nds=sorted(list(enumerate(nd_lgth)),key=lambda x:x[1],reverse = True)
    #print('sorted_nds:',sorted_nds)
    
    #gets the actual node numbers from sorted list
    nd_order = []
    for t in sorted_nds:
        nd_order.append(t[0])
    #print('nd_order:',nd_order)
    
    solution=greedy(neigh_nds,nd_order)
    solution=OrderedDict(sorted(solution.items()))
    sol=list(solution.values())
    #print('color_sort:',color_sort(sol))
    #loop greedy and sorting
    for i in tqdm(range(maxit)):
        #group nodes by color
        chr_sort_sol=color_sort(sol)
        
        #sort nodes by nbr of neighbors
        chr_deg_sol_list=[]
        for i in chr_sort_sol:
            chr_deg_sol=sorted(i,key=lambda x:nd_lgth[x],reverse=True)
            chr_deg_sol_list.append(chr_deg_sol)
        #print('color order sort:',chr_deg_sol_list) 
        
        #make random permutation of colors and extend list
        nd_order=[]
        rand_perm=np.random.permutation(len(chr_deg_sol_list))
        for i in rand_perm:
            nd_order.extend(chr_deg_sol_list[i])     
        #print('new nd_order:',nd_order)
        
        #find new solution
        solution=greedy(neigh_nds,nd_order)
        solution=OrderedDict(sorted(solution.items()))
        sol=list(solution.values())
        #print('')
        #end loop
        
    #chrom_nbr=print(max(solution.values()))   
    output_data = str(max(sol)+1) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, sol))
    return output_data
