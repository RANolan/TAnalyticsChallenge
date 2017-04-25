#!/usr/bin/env python

import os
import sys
import fnmatch
import string
import random
import collections
import csv
import operator
import pandas as pd
from collections import defaultdict

def main(argv):

    Dict1 = {}
    columns = defaultdict(list) # each value in each column is appended to a list
    
    with open('DataReal.csv') as f:
        reader = csv.DictReader(f)     # read rows into a dictionary format
        for row in reader:             # read a row as {column1: value1, column2: value2,...}
            for (k,v) in row.items():  # go over each column name and value 
                columns[k].append(v)   # append the value into the appropriate list
                                       # based on column name k
    

    #Take CSV files and convert into dict in this format...
    #
    #Dict1 = {Date1:{item1:qty1, item2:qty3, item3:qty1}
    #         Date2:{item2:qty1, item3:qty2, item4:qty1} 
    #          ...     }

    count = 1
    for x in range(len(columns['SLS_DTE_NBR'])-1):
        #if date is in dictionary
        if columns['SLS_DTE_NBR'][count] in Dict1: 
            #if item is listed under that date
            if columns['PROD_NBR'][count] in Dict1[columns['SLS_DTE_NBR'][count]]:
                #add QTY to current QTY
                Dict1[columns['SLS_DTE_NBR'][count]][columns['PROD_NBR'][count]] = Dict1[columns['SLS_DTE_NBR'][count]][columns['PROD_NBR'][count]] + int(columns['SLS_QTY'][count])
            else:  
                #Create new item under date
                Dict1[columns['SLS_DTE_NBR'][count]][columns['PROD_NBR'][count]] = int(columns['SLS_QTY'][count])
        else:
            #Create new date in dict
            Dict1[columns['SLS_DTE_NBR'][count]] = {}        
            Dict1[columns['SLS_DTE_NBR'][count]][columns['PROD_NBR'][count]] = int(columns['SLS_QTY'][count])
        count = count+1

    
##################
    count = 0
    for key,value in Dict1.items():
        #if :
        print key[0]
        #print "\n"
        print value
        #print "\n"
        #else:    

        count = count+1
##################

    #print Dict1
    #sorteddict = sorted(Dict1.items(), key=operator.itemgetter(0))
    #print sorteddict

    #print Dict1
    print len(Dict1)
    print len(columns['SLS_QTY'])
    print len(columns['PROD_NBR'])
    print len(columns['SLS_DTE_NBR'])

# begin gracefully
#
if __name__ == "__main__":
    main(sys.argv[0:])
#
# end of file
