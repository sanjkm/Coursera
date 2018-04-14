#!/usr/bin/python
# -*- coding: utf-8 -*-

# solver_branch.py
# Uses relaxation estimates to search for knapsack solutions

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight', 'density'])

from operator import attrgetter, itemgetter
import time
from bisect import bisect_right
from copy import copy
import math, itertools
# class that tracks status of tree traversal
# This tracks total value, remaining capacity, and highest possible
# value for the complete knapsack 

def fillItemList (lines):
    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items,total_wt, total_val = [], 0, 0
    
    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        density = float ((1.0 * int(parts[0]))/int(parts[1]))
        items.append(Item(i-1, int(parts[0]), int(parts[1]), density))
        total_wt += items[-1].weight
        total_val += items[-1].value
    return items, item_count, capacity, total_wt, total_val

# This will calculate the proper allocation for all items and return as a list,
# given an input of an allocation and a list of items. List of items may be out of
# order or incomplete
def fillItemAllocation(alloc, item_list, item_count):

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

def calcMinWeight (items):
    min_weight = None
    for item in items:
        if min_weight == None:
            min_weight = item.weight
        else:
            min_weight = min(min_weight, item.weight)
    return min_weight

# creates a list where each index is the cumulative sum of the weights or values
# before it. The inputted list is effectively reversed before doing this calculation,
# so the zero-th index contains the last weight, 1st index = last + second to last, ...
def calcResidFields (item_list, item_count):
    resid_wt_list, resid_val_list = [], []
    total_wt, total_val = 0, 0
    
    for i in range(item_count):
        rel_index = item_count - 1 - i
        total_wt += item_list[rel_index].weight
        total_val += item_list[rel_index].value

        resid_wt_list.append (total_wt)
        resid_val_list.append (total_val)
        
    return resid_wt_list, resid_val_list

        
def returnToOriginalOrder (alloc_list, items):
    alloc_tuples = []
    for i in range(len(items)):
        alloc_tuples.append((alloc_list[i], items[i].index))
    alloc_tuples = sorted(alloc_tuples, key=itemgetter(1))
    return map(lambda x:x[0], alloc_tuples)

# Takes the difference between the 90th percentile element and the 10th percentile element as the
# range of the dataset. Assumes list is sorted
# This is divided by the median for normalization purposes
def calcVariation (items):
    hi_percentile, lo_percentile = 0.9, 0.1
    med_percentile = 0.5
    item_count = len(items)

    variation = math.fabs ((items[int(hi_percentile*item_count)].density) - \
                (items[int(lo_percentile*item_count)].density))

    med =  math.fabs (items[int(med_percentile*item_count)].density)

    return (1.0 * variation) / med

    
 
# Given the current items in the knapsack, this calculates the largest
# possible value attainable, not taking into account weights of unseen items
def calcSimpleEstimate (curr_value, curr_weight, total_rem_value, capacity):
    
    estimate = curr_value + total_rem_value
    return estimate

def calcFastEstimate (curr_value, curr_weight, resid_wt_list, resid_val_list,
                      capacity):
    rem_capacity = capacity - curr_weight
    estimate = 0
    
    # checks if total weight of remaining lefts is less than remaining capacity
    if resid_wt_list[-1] <= rem_capacity:
        estimate = resid_val_list[-1]
    elif len(resid_wt_list) == 1:
        estimate = 0        
    else:
        locate_key = resid_wt_list[-1] - rem_capacity # want to find this number in list
        index = bisect_right (resid_wt_list, locate_key)

        frac = (1.0 * (resid_wt_list[index] - locate_key)) / \
               (resid_wt_list[index] - resid_wt_list[index - 1])

        estimate = (resid_val_list[-1] - resid_val_list[index]) + \
                   frac * (resid_val_list[index] - resid_val_list[index - 1])

    return (curr_value + estimate)
    
def simpleTreeTraverse (remaining_items, capacity, curr_value,
                        curr_weight, top_overall,
                        resid_wt_list, resid_val_list, min_wt, estimate_type=None):
    final_alloc, best_result = [], top_overall # default
    item_value, item_weight = remaining_items[0].value, remaining_items[0].weight
    
    for x_i in [1,0]: # either go left or go right
        # conditions preventing adding the item to the knapsack
        if x_i == 1:
            if (curr_weight + item_weight) > capacity:
                continue
        
        test_weight = curr_weight + (x_i)*item_weight + min_wt    
        if len(remaining_items) == 1 or test_weight > capacity:  # tree ending conditions
            curr_alloc, curr_result = [x_i], curr_value + (x_i)*item_value
            if curr_result > best_result:
                final_alloc, best_result = curr_alloc, curr_result
                
        else:  # remaining options to choose from
            # if best estimate less than best_result, no need to traverse
            if estimate_type == 'Fast':
                if calcFastEstimate (curr_value + (x_i)*item_value,
                                     curr_weight + (x_i)*item_weight, resid_wt_list[:-1],
                                     resid_val_list[:-1], capacity) < best_result:
                    continue
            
            elif estimate_type == 'Simple':
                if calcSimpleEstimate (curr_value, curr_weight,
                                       resid_val_list[-1] - item_value, capacity) < best_result:
                    continue
            
            iter_alloc, iter_result =  simpleTreeTraverse (remaining_items[1:],
                                                           capacity,
                                                           curr_value + x_i*item_value,
                                                           curr_weight+ x_i*item_weight,
                                                           best_result,
                                                           resid_wt_list[:-1],
                                                           resid_val_list[:-1],
                                                           min_wt, estimate_type)
 
            curr_alloc, curr_result = [x_i] + iter_alloc, iter_result
            
            if curr_result > best_result:
                final_alloc, best_result = curr_alloc, curr_result
    return final_alloc, best_result


def noDensityTreeTraverse (remaining_items, capacity, curr_value,
                        curr_weight, top_overall,
                        resid_wt_list, resid_val_list, min_wt,
                           small_wt_list, small_wt_dict,
                           min_small_wt, small_wt_count, estimate_type=None):
    
    final_alloc, best_result = [], top_overall # default
    item_value, item_weight = remaining_items[0].value, remaining_items[0].weight
    
    for x_i in [1,0]: # either go left or go right
        # conditions preventing adding the item to the knapsack
        if x_i == 1:
            if (curr_weight + item_weight) > capacity:
                continue
        
        test_weight = curr_weight + (x_i)*item_weight + min_wt    
        if len(remaining_items) == 1 or test_weight > capacity:  # tree ending conditions
            curr_alloc, curr_result = [x_i], curr_value + (x_i)*item_value

            # Find the best possible result using the smallest weight items
            remaining_weight = capacity - curr_weight
            if remaining_weight > min_small_wt:  # can't add without exceeding capacity
                curr_alloc = [x_i] + [0]*small_wt_count
            else:                
                index = bisect_right (small_wt_list, remaining_weight)
                small_weight = small_wt_list[index-1]
                curr_weight += small_weight
                curr_result += small_wt_dict[small_weight][0]
                curr_alloc = curr_alloc + list(reversed(small_wt_dict[small_weight][1]))
                
            if curr_result > best_result:
                final_alloc, best_result = curr_alloc, curr_result
                
        else:  # remaining options to choose from
            # if best estimate less than best_result, no need to traverse
            if calcSimpleEstimate (curr_value, curr_weight,
                                   resid_val_list[-1] - item_value, capacity) < best_result:
                continue
            
            iter_alloc, iter_result =  noDensityTreeTraverse (remaining_items[1:],
                                                           capacity,
                                                           curr_value + x_i*item_value,
                                                           curr_weight+ x_i*item_weight,
                                                           best_result,
                                                           resid_wt_list[:-1],
                                                           resid_val_list[:-1],
                                                           min_wt,
                                                           small_wt_list, small_wt_dict,
                                                           min_small_wt, small_wt_count,
                                                           estimate_type)
 
            curr_alloc, curr_result = [x_i] + iter_alloc, iter_result
            
            if curr_result > best_result:
                final_alloc, best_result = curr_alloc, curr_result
    return final_alloc, best_result




# This determines the type of best estimate to use for the tree traversal, and then
# returns the best result and allocation if it is superior to the existing best result
def executeTreeTraverse (items, capacity, best_result, item_count):
    field_list = ['density', 'value']
    items = sortByField(items, field_list)
    
    # calc variation of the density of the items
    variation_perc = calcVariation (items)
    print variation_perc
    if variation_perc > 0.0000001:
        estimate_type = 'Fast'
    else:
        estimate_type = 'Simple'
        field_list = ['weight']
        items = sortByField (items, field_list)
    
    resid_wt_list, resid_val_list = calcResidFields (items, len(items))
    value, weight = 0,0
    min_weight = calcMinWeight(items)

    if estimate_type == 'Fast':
    
        new_alloc, new_result =  simpleTreeTraverse (items, capacity, value, weight,
                                                 best_result, resid_wt_list,
                                                 resid_val_list, min_weight,
                                                estimate_type)
    elif estimate_type == 'Simple':

        small_wt_count = min(20, int(0.25 * len(items)))
        items_ex_small = items[:(-1 * small_wt_count)]
        min_weight = calcMinWeight (items_ex_small)
        min_small_wt = calcMinWeight (items[(-1 * small_wt_count):])

        small_wt_list, small_wt_dict = calcAllRelevantSums (items[(-1 * small_wt_count):],
                                                            capacity)
        
        new_alloc, new_result =  noDensityTreeTraverse (items_ex_small, capacity, value,
                                                        weight, best_result,
                                                        resid_wt_list, resid_val_list,
                                                        min_weight,
                                                        small_wt_list, small_wt_dict,
                                                        min_small_wt, small_wt_count,
                                                        estimate_type=None)
    
    if new_result > best_result:
        new_alloc = fillItemAllocation(new_alloc, items, item_count)
        return new_alloc, new_result
    return [], best_result


# Find all items whose weight plus the 10th percentile item puts total over
# capacity
# Calculate best alloc for these large items, and take all of these items out of# the item list for future calculation because they are done
def largeWeightItems (items, capacity, perc_thresh):

    field_list, item_count = ['weight'], len(items)
    items = sortByField (items, field_list, False)
    min_weight = items[0].weight
    
    cutoff_index = int(perc_thresh * item_count)
    weight_cutoff = items[cutoff_index].weight
    small_weight_list = items[:cutoff_index + 1]
    
    target_index = item_count # smallest item at desired weight target
    while items[target_index - 1].weight >= (capacity - weight_cutoff):
        target_index -= 1
        if target_index <= 0:
            break
    if target_index == item_count: # no items satisfy weight requirement
        return items, [], 0

    target_index = min(max(target_index, cutoff_index+1), item_count-1)

    best_result = 0
    for index in range(item_count - 1, target_index - 1, -1):  
        new_alloc, new_result = simpleTreeTraverse ([items[index]] + small_weight_list,
                                                    capacity, 0, 0, best_result,
                                                    [], [], 0, min_weight)
        if new_result > best_result:
            best_alloc, best_result = new_alloc, new_result
            key_index = index

    best_alloc = fillItemAllocation (best_alloc, [items[key_index]] + small_weight_list,
                                     item_count)
    print target_index
    return items[:target_index], best_alloc, best_result 

# Function calculates all possible combinations of items such that the
# weight sum is less than or equal to capacity
# It outputs a sorted list of the associated weight sums, as well as a
# dictionary mapping the weight to its total value and the item allocation list
# that generates it
def calcAllRelevantSums (items, capacity):
    field = ['weight']
    items_sorted = sortByField (items, field, False)
    # determine max number of items such that weight sum greater than capacity
    max_item_count, wt_sum, i = 0,0,0
    if capacity > 0:
        while wt_sum <= capacity:
            wt_sum += items_sorted[max_item_count].weight
            max_item_count += 1
            if max_item_count == len(items):
                break
    # generate all alloc possibilities
    bin_choices = [0,1]
    alloc_list = itertools.product(*([bin_choices]*len(items)))

    # generate list of weights, and dictionary
    weight_list, weight_dict = [], {}
    for alloc in alloc_list:
        if sum(alloc) >= max_item_count:
            continue
        wt_sum = sum([items[i].weight*alloc[i] for i in range(len(items))])
        if wt_sum > capacity:
            continue
        val_sum = sum([items[i].value*alloc[i] for i in range(len(items))])
        weight_list.append(wt_sum)
        weight_dict[wt_sum] = (val_sum, alloc)
        
    return sorted(weight_list), weight_dict

                                   
    
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
    # parse the input
    lines = input_data.split('\n')

    items, item_count, capacity, total_val, total_wt = fillItemList (lines)
    orig_items = copy(items)

    start_time = time.time()

#    print calcAllRelevantSums (items, capacity)
#    print time.time() - start_time
#    exit(0)
    
    # Initial greedy estimate
    best_alloc, best_result = initGreedyEstimate(items, capacity)

    # Check large estimate
    items_ex_large, new_alloc, new_result = largeWeightItems (items, capacity, 0.1)

    if new_result > best_result:
        best_alloc, best_result = new_alloc, new_result

    # Do relaxed search
    new_alloc, new_result = executeTreeTraverse (items_ex_large, capacity, best_result,
                                                 len(items))
    if new_result > best_result:
        best_alloc, best_result = new_alloc, new_result
    
    print time.time() - start_time
    return solveOutput (best_alloc, best_result, orig_items, capacity)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

