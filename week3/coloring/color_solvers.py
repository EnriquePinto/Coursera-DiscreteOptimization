from constraint import *
import numpy as np
from collections import Counter, OrderedDict
from math import floor,ceil

# utilizar o alldiferent para cada nó
def solver_dec(input_data):
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
    print('max connex:',connex_count)
    
    def dif_const(c1, c2):
        if c1 != c2:
            return True

    def sim_brk_const(x):
        if x == 0:
            return True
    
    for i in range((connex_count+1),1,-1):
        #print('i:',i)
        # declares constr. prog. problem
        g_color = Problem(RecursiveBacktrackingSolver())
        # declare all variables
        g_color.addVariables(range(node_count), range(i))   
        
        for e in edges:
            g_color.addConstraint(dif_const, (e[0], e[1]))
    
        for n in range(node_count):
            g_color.addConstraint(NotInSetConstraint([n]),neigh_nds[n])

        g_color.addConstraint(sim_brk_const, [0])
    
        solution = g_color.getSolution()
        if solution==None:
            print("No solutions found for c=",i,"\n")
            print("Using solution for c=",i+1)
            solution=prev_sol
            break
        else:
            print("sol c=",i,"||",end='')
            solution=OrderedDict(sorted(solution.items()))
            prev_sol=solution
    
    # prepare the solution in the specified output format
    output_data = str(node_count) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution.values()))
    return output_data

def solver_asc(input_data):
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
    print('max connex:',connex_count)

    def dif_const(c1, c2):
        if c1 != c2:
            return True

    def sim_brk_const(x):
        if x == 0:
            return True

    for i in range(2,(connex_count+2)):
        # declares constr. prog. problem
        g_color = Problem(RecursiveBacktrackingSolver())
        # declare all variables
        g_color.addVariables(range(node_count), range(i))   
        
        for e in edges:
            g_color.addConstraint(dif_const, (e[0], e[1]))

        for n in range(node_count):
            g_color.addConstraint(NotInSetConstraint([n]),neigh_nds[n])

        g_color.addConstraint(sim_brk_const, [0])

        solution = g_color.getSolution()
        if solution==None:
            print("no sol c=",i,"||",end='')           
        else:
            print("!>sol c=",i,"<!")
            solution=OrderedDict(sorted(solution.items()))
            break

    # prepare the solution in the specified output format
    output_data = str(node_count) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution.values()))
    return output_data

def solver_bisec(input_data):
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

    a=2
    b=connex_count+1
    m=floor((a+b)/2)
    if node_count>600:
        m=124
        maxit=1
    elif node_count>300:
        maxit=5
    else:
        maxit=10
    print('Maxit=',maxit)
    
    for i in range(maxit):
        print('a:',a,', b:',b)
        print('Trying c=',m,'| it=',i)
        # declares constr. prog. problem
        g_color = Problem(MinConflictsSolver())
        # declare all variables
        g_color.addVariables(range(node_count), range(m))   
        
        for e in edges:
            g_color.addConstraint(dif_const, (e[0], e[1]))
    
        for n in range(node_count):
            g_color.addConstraint(NotInSetConstraint([n]),neigh_nds[n])

        g_color.addConstraint(sim_brk_const, [0])
    
        solution = g_color.getSolution()
        if solution==None:
            #print('\n a:',a,', b:',b)
            print("no sol c=",m)
            if floor((m+b)/2)==m or (i==maxit-1):
                print('Using Saved Solution! c=',saved_m)
                solution=saved_sol
                break
            a=m
            m=floor((m+b)/2)          
        else:
            #print('\n a:',a,', b:',b)
            print("sol c=",m)
            saved_m=m
            if floor((m+a)/2)==m:
                print('Using found solution! c=',m)
                break
            saved_sol=solution
            b=m
            m=floor((m+a)/2)       
    print('Done!')       
    #if i==(maxit-1):
    #    opt=0
    #else:
    #    opt=1     
    opt=0 
    solution=OrderedDict(sorted(solution.items()))
    # prepare the solution in the specified output format
    output_data = str(saved_m) + ' ' + str(opt) + '\n'
    output_data += ' '.join(map(str, solution.values()))
    return output_data