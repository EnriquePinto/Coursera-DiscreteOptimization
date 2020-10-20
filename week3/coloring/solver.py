#!/usr/bin/python
# -*- coding: utf-8 -*-
from color_solvers import solver_bisec
from stubborn_solver import stubborn_solver
from greedy_solver import it_greedy_solver

def solve_it(input_data):
    # Modify this code to run your optimization algorithm
    output_data=it_greedy_solver(input_data,10000)
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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

