#! /usr/bin/env python

# PonyGE2
# Copyright (c) 2017 Michael Fenton, James McDermott,
#                    David Fagan, Stefan Forstenlechner,
#                    and Erik Hemberg
# Hereby licensed under the GNU GPL v3.
""" Python GE implementation """
from utilities.algorithm.general import check_python_version
import sys
sys.path.append('D:\\PythonCode\\PonyGE2-master\\src')
from ant import Ant
import numpy as np
from utilities.stats import trackers

check_python_version()

from stats.stats import get_stats
from algorithm.parameters import params, set_params


''' Santa Fe Trail initialisation '''
with open('santa_fe_trail.txt') as f:
    santa_fe_trail_graph = []
    for line in f.readlines():      
        santa_fe_trail_graph.append(line[:32])

santa_fe_trail = np.zeros((32,32))
for y in range(32):
    for x in range(32):
        if santa_fe_trail_graph[y][x] == 'x':
            santa_fe_trail[y][x] = 1



def mane():
    """ Run program """

    # Run evolution
    individuals = params['SEARCH_LOOP']()

    # Print final review
    get_stats(individuals, end=True)


if __name__ == "__main__":
    set_params(sys.argv[1:])  # exclude the ponyge.py arg itself # sys.argv[1:] is the parametre we input in the command line
    mane()
    print('\n\n')
    print(trackers.fitness_store)
    print(trackers.best_count)
    print(trackers.genome_len)
