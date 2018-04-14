#!/usr/bin/python
# -*- coding: utf-8 -*-
# solver_dp_final.py
# uses dynamic programming to solve knapsack problem

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

from operator import attrgetter, itemgetter
import itertools
import time, os, sys
from bisect import bisect_left
from heapq import merge


# Sorts a sequence, removing duplicate elements
def sort_uniq(sequence):
    return list(itertools.imap(itemgetter(0), itertools.groupby(sorted(sequence))))


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

# Given a Dynamic Programming tree, traces back the tree to find the item allocation
# corresponding to the value inputted
# Program assumes that items is sorted in the order in which the DP change_list column files were
# generated
# Alloc will be returned in the order that items is currently sorted in
def traceBackAllocation (items, final_tuple, change_list):

    best_val, best_weight = final_tuple[0], final_tuple[1]
    item_num = len(items)
    
    alloc = [0] * (item_num + 1)  # using this size so that alloc[i] corresponds to the
                                  # ith item, as the change_list is labeled that way. Will drop
                                  # first element at program end
    test_weight = best_weight
    test_index = item_num
    while test_weight > 0:
        while test_weight not in change_list[test_index]:
            test_index -= 1
        alloc[test_index] = 1
        test_weight = test_weight - items[test_index - 1].weight
        test_index -= 1        
    del alloc[0]
    return alloc


def calcListBreakpointValue (prev_bp_list, curr_bp, index):
    
    i = index
    while (prev_bp_list[i][1] < curr_bp):
        i += 1
        if i == len(prev_bp_list):
            break
        
    if i == 0:
        curr_val = prev_bp_list[0][0]
        curr_index = i
    elif i == len(prev_bp_list):
        curr_val = prev_bp_list[i-1][0]
        curr_index = i - 1
    else:
        if prev_bp_list[i][1] == curr_bp:
            curr_val = prev_bp_list[i][0]
            curr_index = i
        else:
            curr_val = prev_bp_list[i-1][0]
            curr_index = i - 1
    return curr_val, curr_index
            
# Uses list of previous breakpoints to determine the current breakpoint value
def calcFastBreakpointValue (curr_bp, prev_bp_list, curr_index,
                             item, lag_index):

    curr_val, new_index = calcListBreakpointValue (prev_bp_list, curr_bp, curr_index)
    if curr_bp < item.weight:
        new_val = curr_val
    else:
        lag_val, lag_index = calcListBreakpointValue (prev_bp_list, curr_bp - item.weight, lag_index)
        if curr_val < (lag_val + item.value):
            return (lag_val + item.value), new_index, lag_index, 1
        return curr_val, new_index, lag_index, 0

    return new_val, new_index, lag_index, 0

# Creates the DP table for the knapsack problem, leading to the optimal value in the
# last column, last row
# Program does not store the table though. It only stores the rows(weights) whose optimal value changes
# when adding in item i (i.e. n will be stored in change_compilation[i] if the value in the nth row of the DP table
# changed between columns (i-1) and i
# This change table is used to calculate the allocation that leads to this optimal value
# Columns of the table are calculated as a series of 'breakpoints': the rows where the optimal value
# changes
def dynamicProgrammingSolution (items, capacity):
    field = ['weight']
    items_sorted = items
    counter, i, mem_flag, delim = 0, 0, 0, ','
    curr_bp_list, prev_bp_list = [], []
    weight_breakpoints = [0]  # this is the list of indices in the table for which the best value changes
    prev_bp_list = [(0,0)]
    change_compilation = [[0]]   # the zeroth column change of the DP table
    counter += 1
    
    for item in items_sorted:
        change_list = []  # list of weights where the value increases from the previous column
        next_weight_breakpoints = [(item.weight + n) for n in weight_breakpoints
                                   if (item.weight + n) <= capacity]
        weight_breakpoints = sort_uniq (weight_breakpoints + next_weight_breakpoints)
        
        i = 0
        fut_weight_breakpoints = []
        exp_val, new_val = 0, 0
        curr_index, lag_index = 0,0

        while i < len(weight_breakpoints):
            curr_bp = weight_breakpoints[i]
            exp_val, curr_index, lag_index, flag =  calcFastBreakpointValue (curr_bp, prev_bp_list,
                                                                       curr_index, item, lag_index)
            if flag == 1:  # value changed from previous column
                change_list.append (curr_bp)
            if len(curr_bp_list) > 0:
                if exp_val == curr_bp_list[-1][0]: # not a breakpoint
                    i += 1
                    continue
            curr_bp_list.append((exp_val, curr_bp))
            fut_weight_breakpoints.append(curr_bp)
            i += 1

        prev_bp_list = curr_bp_list[:]
        curr_bp_list = []
        weight_breakpoints = fut_weight_breakpoints[:]
        change_compilation.append (change_list)

        counter += 1
    best_value = max(exp_val, new_val)

    return best_value, prev_bp_list[-1], change_compilation

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

    items, capacity = fillItems (input_data)
    
    start_time = time.time()
    sort_field = ['weight']
    items_sorted = sortByField (items, sort_field)
    
    best_result, final_tuple, change_list = dynamicProgrammingSolution (items_sorted, capacity)
    
    alloc = traceBackAllocation (items_sorted, final_tuple, change_list)
    
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

