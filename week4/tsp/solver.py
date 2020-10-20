#!/usr/bin/python
# -*- coding: utf-8 -*-

from sim_annealing_solver import annealing_solver
from annealing_solver_2 import new_annealing_solver
from two_opt_solver import two_opt_solver
from tsp_mip import tsp_mip_solver
from threeopt_teste import threeopt_annealing
from twoopt_search import twoopt_solver

def solve_it(input_data):
    
    output_data=twoopt_solver(input_data)

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

