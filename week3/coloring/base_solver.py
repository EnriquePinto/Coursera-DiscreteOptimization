from constraint import *
import numpy as np
from collections import Counter, OrderedDict

# utilizar o alldiferent para cada nó
def base_solv(input_data):
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
    
    #discovers maximum connections 
    nd_lgth=[]
    for n in neigh_nds:
        nd_lgth.append(len(n))
    
    connex_count=max(nd_lgth)
    print('max connex:',connex_count)
    max_connex_nd=np.argmax(nd_lgth)
    print(max_connex_nd)
    
    def dif_const(c1, c2):
        if c1 != c2:
            return True

    def sim_brk_const(x):
        if x == 1:
            return True
    
    for i in range(2,(connex_count+2)):
        # declares constr. prog. problem
        g_color = Problem()
        # declare all variables
        g_color.addVariables(range(node_count), range(i))
        
        for e in edges:
            g_color.addConstraint(dif_const, (e[0], e[1]))
    
        for n in range(node_count):
            g_color.addConstraint(NotInSetConstraint([n]),neigh_nds[n])

        g_color.addConstraint(sim_brk_const, [0])
    
        solution = g_color.getSolution()

        if solution is None:
            print("No solutions found for c=",i)
        else:
            solution=OrderedDict(sorted(solution.items()))
            break
    
    # prepare the solution in the specified output format
    output_data = str(node_count) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution.values()))
    return output_data