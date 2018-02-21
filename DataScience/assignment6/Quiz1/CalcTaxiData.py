# CalcTaxiData.py

import math
import csv

def mean_calc(x):
    if len(x) == 0:
        print "Error - no mean because no record"
        exit(1)
    return (1.0*sum(x)) / len(x)

def sampleMeanStdDev (x):

    if len(x) <= 1:
        print "Not enough data for stdev"
        exit(1)
    mean = mean_calc(x)

    SSE = sum([(val - mean)*(val-mean) for val in x])

    return math.sqrt(SSE / (len(x) * (len(x) - 1)))

def samplePropStdDev (x):
    if len(x) <= 1:
        print "Not enough data for stdev"
        exit(1)
    p = mean_calc(x)
    n = len(x)
    
    return math.sqrt(p * (1-p) / n)

def getData (data_file, delim):
    data_list, test_dict = [], {}
    with open (data_file, 'rb') as csvfile:
        datareader = csv.reader(csvfile, delimiter=delim)
        for row in datareader:
            field_list = row
            break
        index = 0
        for row in datareader:
            if index == 0:
                index += 1
                continue
            for i in range(len(row)):
                test_dict[field_list[i]] = row[i]
            data_list.append(dict(test_dict))
                
    csvfile.close()
    return data_list

def getFieldData (data_list, field_name, binary=False, field_val=0):
    field_list = []
    for row in data_list:
        if binary == False:
            field_list.append (float(row[field_name]))
        else:
            if row[field_name] == str(field_val):
                field_list.append(1)
            else:
                field_list.append(0)
    return field_list

def calcFieldStats (field_data_list, binary_flag, conf_level):
    if conf_level == 0.95:
        z = 1.96
    if conf_level == 0.99:
        z = 2.5758

    mean = mean_calc(field_data_list)

    if binary_flag == True:
        sample_stdev =  samplePropStdDev(field_data_list)

    else:
        sample_stdev =  sampleMeanStdDev(field_data_list)
    print "Sum Count", sum(field_data_list)
    print "Average", mean
    print "Std Dev Estimate", sample_stdev
    print "Confidence Interval:"
    print "(%f, %f)" % (mean - z*sample_stdev, mean + z * sample_stdev)
        
    

def fieldParameterList():
    param_list = []
    param1 = ("payment_type", True, 2, 0.99)
    param_list.append(param1)

    param2 = ("trip_distance", False, 0, 0.95)
    param_list.append(param2)
    return param_list

def main():
    data_file = "taxisample10000.csv"
    delim = ','
    data_list = getData (data_file, delim)

    param_list = fieldParameterList()

    for param in param_list:
        field_name, bin_flag = param[0], param[1]
        field_val, conf_level = param[2], param[3]
        
        field_data_list = getFieldData (data_list,field_name,
                                        bin_flag, field_val)
        calcFieldStats (field_data_list, bin_flag, conf_level)

main()
    
                  

                    
    
