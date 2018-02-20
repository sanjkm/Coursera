# GetStopCount.py
# Get the total words and the total stop words from the Hadoop counters
# within the log files
# Majority of this program derives the name of the appropriate file
# from which to get the data

# Application job ID string is fed into program as an argument from stdin

import sys
import json

LogDir = "/tmp/hadoop-yarn/staging/history/done_intermediate/jovyan/"

# Takes as input the Application job ID
# Opens the summary file named after that ID, extracts data from the file,
# outputs name of the json summary history file
def DeriveSummaryFileName (Application_ID):
    
    infileName = 'job_' + Application_ID 
    suffix =  '.summary'
    init_sep, arg_sep = ',', '='
    arg_dict = {}
    
    with open(infileName + suffix, 'r') as f:
        for line in f:
            fields = (line.strip()).split(init_sep)
            for field in fields:
                x_field = field.split(arg_sep)
                desc, val = x_field[0], x_field[1]
                arg_dict[desc] = val
            break
    f.close()

    FieldOrderList = ['submitTime', 'user', 'jobName', 'finishTime',
                      'numMaps', 'numReduces', 'status', 'queue',
                      'launchTime']
    out_suffix = '.jhist'

    SpaceReplChar = '%2B'
    
    FieldList = [infileName] + [arg_dict[desc].replace(' ',SpaceReplChar)
                                for desc in FieldOrderList]

    filename = '-'.join(FieldList) + out_suffix

    return filename
    

def main():
    
    for line in sys.stdin:
        CounterFileName = DeriveSummaryFileName (str(line.strip()))
        break

    
    
        
main()
