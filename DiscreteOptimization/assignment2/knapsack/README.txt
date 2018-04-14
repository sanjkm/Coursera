Progams in this directory will output the optimal knapsack given a file
containing knapsack parameters. 

Programs:
solver_dp.py - Solves the knapsack problem using dynamic programming. This was
an initial attempt at the problem

solver_dp_final.py - Much faster program using dynamic programming

solver_branch.py - Solves the program using a recursive branch and bound
estimate technique. This can run faster than the DP programs when the knapsack
items have high variation of value / weight ratios. It is limited by
Python's recursion limit though, as to the size of the sample space

Directory:
data - Contains different knapsack files. File label indicates the number of
items to choose from. First line of each file lists the total number of items and the 
total knapsack capacity K. Each line afterward lists the value and the weight
of the item, for each item in the knapsack
