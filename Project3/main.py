import random

from pivotFirst import quick_sort_pivot_first
from pivotMedianofThree import quick_sort_pivot_median_of_three
from pivotPermutated import quick_sort_pivot_permutated
from pivotRandom import quick_sort_pivot_random
import sys
from inputCreator import create_input
from time import perf_counter

sys.setrecursionlimit(150000)
algorithms = {'Ver1': quick_sort_pivot_first,
              'Ver2': quick_sort_pivot_random,
              'Ver3': quick_sort_pivot_permutated,
              'Ver4': quick_sort_pivot_median_of_three,
              }

cases = {'Worst Case': 'worst',
         'Average Case': 'average'}

input_types = {'Type 1': 1,
               'Type 2': 2,
               'Type 3': 3,
               'Type 4': 4}

sizes = [100, 1000, 10000]
file = open("output2.txt", 'w')
file.close()
file = open("output2.txt", "a")
for size in sizes:
    for type_name, type_value in input_types.items():
        text = f'Size: {size}, type: {type_name}'
        file.write(text + '\n')
        worst_case_input = create_input('worst', type_value, size)
        file.write('Worst Case Input: '+str(worst_case_input) + '\n')
        average_inputs = []
        for i in range(5):
            average_case_input = create_input('average', type_value, size)
            file.write(f'Average Case Input{i+1}: '+str(average_case_input) + '\n')
            average_inputs.append(average_case_input)
        for algorithm, function in algorithms.items():
            for case_name, case_value in cases.items():
                if case_value == 'average':
                    time_spent = []
                    for inp in average_inputs:
                        copy_arr = inp.copy()
                        if algorithm == 'Ver3':
                            random.shuffle(copy_arr)
                        start = perf_counter()
                        sorted_list = function(copy_arr, 0, size - 1)
                        end = perf_counter()
                        time_spent.append(end-start)
                    text = f"Size: {size}, type: {type_name}, algorithm: {algorithm}, case: {case_name}, time spent: {'{:10.4f}'.format((sum(time_spent)/len(time_spent))*1000)}"
                    file.write(text+'\n')
                elif case_value == 'worst':
                    copy_arr = worst_case_input.copy()
                    if algorithm == 'Ver3':
                        random.shuffle(copy_arr)
                    start = perf_counter()
                    sorted_list = function(copy_arr, 0, size-1)
                    end = perf_counter()
                    time_spent = end-start
                    text = f"Size: {size}, type: {type_name}, algorithm: {algorithm}, case: {case_name}, time spent: {'{:10.4f}'.format(time_spent*1000)}"
                    file.write(text + '\n')
