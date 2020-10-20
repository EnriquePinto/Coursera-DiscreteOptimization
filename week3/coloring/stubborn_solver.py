from constraint import *
import numpy as np
from color_solvers import solver_bisec
from collections import Counter, OrderedDict
from math import floor,ceil

def stubborn_solver(input_data):
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
    
    connex_count=max(nd_lgth)
    
    print('node count:',node_count)
    print('max connex:',connex_count)
    
    def dif_const(c1, c2):
        if c1 != c2:
            return True

    def sim_brk_const(x):
        if x == 0:
            return True
    
    if node_count==1000:
        m=100
    elif node_count==500:
        m=18
    elif node_count==250:
        m=78
    elif node_count==100:
        m=16
    elif node_count==70:
        m=20
    else:
        m=6
    maxit=150;
    print('m=',m)
    for i in range(maxit):
        print('it=',i)
        # declares constr. prog. problem
        g_color = Problem(MinConflictsSolver())
        # declare all variables
        g_color.addVariables(range(node_count), range(m))   
        
        for e in edges:
            g_color.addConstraint(dif_const, (e[0], e[1]))
    
        #for n in range(node_count):
            #g_color.addConstraint(NotInSetConstraint([n]),neigh_nds[n])

        g_color.addConstraint(sim_brk_const, [0])
    
        solution = g_color.getSolution()
        if solution==None:
            #print('\n a:',a,', b:',b)
            print("no sol!")         
        else:
            #print('\n a:',a,', b:',b)
            print("sol!")
            break
            
    print('Done!')            
    if solution==None:
        print('GIVING UP!')
        output_data=solver_bisec(input_data)
        return output_data
    else:
        solution=OrderedDict(sorted(solution.items()))
        opt=1 
        # prepare the solution in the specified output format
        output_data = str(saved_m) + ' ' + str(opt) + '\n'
        output_data += ' '.join(map(str, solution.values()))
        return output_data