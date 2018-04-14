#!/usr/bin/python
# -*- coding: utf-8 -*-
# solver_dp.py
# uses dynamic programming to solve knapsack problem

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

from operator import attrgetter, itemgetter
import itertools
import time, os
from bisect import bisect_left

dyn_list_dir = 'DynList/'
file_prefix = 'item_'


def fillItems (input_data):
    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))
    return items, capacity


# This will calculate the proper allocation for all items and return as a list,
# given an input of an allocation and a list of items. List of items may be out of
# order or incomplete
def fillItemAllocation(alloc, item_list, item_count):

    if len(alloc) > item_count:
        print "Error - alloc has more elements than item_count"
        exit(0)
    
    final_alloc = [0] * item_count
    for i in range(len(alloc)):
        item_index = item_list[i].index
        final_alloc[item_index] = alloc[i]
    return final_alloc


# sorts list of items in reverse by specified fields
def sortByField (item_list, field_list, reverse_flag=True):

    return sorted (item_list, key=attrgetter(*field_list), reverse=reverse_flag)

def initGreedyEstimate (item_list, capacity):
    items = sortByField (item_list, ['weight','value'])
    wt_sum, val_sum, i = 0,0,0
    alloc = []
    
    while i < len(items):
        if (wt_sum + items[i].weight) <= capacity:
            val_sum += items[i].value
            wt_sum += items[i].weight
            alloc.append(1)
        else:
            alloc.append(0)
        i += 1        
    alloc = alloc + [0] * (len(items) - len(alloc))
    alloc = fillItemAllocation(alloc, items, len(items))
    
    return alloc, val_sum

# Goes to the line_num-th line of the file and returns the value located there
# Returns none if line_num is greater than number of lines in file
# Note starts with line zero
def getFileLineNumVal (filename, line_num):
    with open(filename, 'r') as f:
        i, val = 0, None
        for line in f:
            if i == line_num:
                val = int(line.strip())
                break
            i += 1
    f.close()
    return val

# Given a Dynamic Programming tree, traces back the tree to find the item allocation
# corresponding to the value inputted
# Program assumes that items is sorted in the order in which the DP column files were
# generated
# Alloc will be returned in the order that items is currently sorted in
def traceBackAllocation (value, file_num, line_num, items, file_dir, file_prefix):
    # check final file, make sure last column of table contains value on the
    # inputted line number
    if (value != getFileLineNumVal (file_dir + file_prefix + str(file_num), line_num)):
        print 'Error - Value is not located on the inputted line number'
        exit(0)

    alloc = [0] * (file_num + 1)  # using this size so that alloc[i] corresponds to the
                                  # ith item, as the files are labeled that way. Will drop
                                  # first element at program end
    for i in range(file_num, 0, -1):
        item_val = items[i-1].value
        test_wt = items[i-1].weight
        test_line = line_num - test_wt
        test_val = getFileLineNumVal (file_dir + file_prefix + str(i-1), test_line)
        # print test_val, test_line, test_wt, item_val
        # exit(0)
        
        if (value - test_val) == item_val: # item i is in the allocation
            alloc[i] = 1
            line_num, value = test_line, test_val
            if value == 0: # all items have been located
                break
    del alloc[0]
    os.system('rm ' + dyn_list_dir + '*') # deletes all filed created

    return alloc

def dynamicProgrammingSolution (items, capacity):

    field = ['weight']
    total_wt = 0
    items_sorted = items
    counter, i = 0, 0

    with open (dyn_list_dir + file_prefix + str(counter), 'w') as f_item:
        while i < (items_sorted[0].weight + 1):
            f_item.write(str(0) + '\n')
            i += 1
            
    f_item.close()
    prev_list_len = items_sorted[0].weight + 1

    counter += 1
    for item in items_sorted:
        total_wt += item.weight
        with open(dyn_list_dir + file_prefix + str(counter), 'w') as f_item:
            with open(dyn_list_dir + file_prefix + str(counter-1), 'r') as f_prev:
                with open(dyn_list_dir + file_prefix + str(counter-1), 'r') as f_prev_lag:
                    i = 0
                    while i < (min(capacity, total_wt) + 1): # i represents capacity
                        if i < item.weight and i < prev_list_len:
                            prev_val = int((f_prev.readline()).strip())
                            new_val = prev_val

                        elif i < item.weight and i >= prev_list_len:
                            new_val = prev_val

                        elif i >= item.weight and i < prev_list_len:
                            prev_val = int((f_prev.readline()).strip())
                            prev_lag_val =  int((f_prev_lag.readline()).strip())
                            new_val = max(prev_val, prev_lag_val + item.value)

                        elif i >= item.weight and i >= prev_list_len:
                            prev_lag_val =  int((f_prev_lag.readline()).strip())
                            new_val = max(prev_val, prev_lag_val + item.value)

                        f_item.write (str(new_val) + '\n')
                        i += 1
                    prev_list_len = min(capacity, total_wt) + 1
                    counter += 1
                f_prev_lag.close()
            f_prev.close()
        f_item.close()
        
    best_value = new_val
    return best_value

def checkSolution (alloc, items):
    total_val, total_wt = 0,0
    for i in range(len(items)):
        total_val += alloc[i]*items[i].value
        total_wt += alloc[i]*items[i].weight
    return total_val, total_wt

def solveOutput (best_alloc, best_result, items, capacity):
    print capacity
    print checkSolution (best_alloc, sortByField(items, ['index'], False))
    # prepare the solution in the specified output format
    output_data = str(best_result) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, best_alloc))
    return output_data

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    items, capacity = fillItems (input_data)
    
    start_time = time.time()
    sort_field = ['weight']
    items_sorted = sortByField (items, sort_field)    
    best_result = dynamicProgrammingSolution (items_sorted, capacity)
    
    alloc = traceBackAllocation (best_result, len(items), capacity,
                                 items_sorted, dyn_list_dir, file_prefix)
    best_alloc = fillItemAllocation (alloc, items_sorted, len(items))
    print time.time() - start_time
    return solveOutput (best_alloc, best_result, items, capacity)


if __name__ == '__main__':

    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

