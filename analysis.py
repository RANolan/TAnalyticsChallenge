#!/usr/bin/env python
import datetime
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
from collections import Counter


##################
# usage of program is python analysis.py 'path to dataset' 'path to csv of product keys and names'
# current example     python analysis.py DataReal.csv prod_keys.csv
##################


def main(argv):

    Dict1 = {}
    columns = defaultdict(list) # each value in each column is appended to a list
    
    with open(argv[1], "r") as f:
        reader = csv.DictReader(f)     # read rows into a dictionary format
        for row in reader:             # read a row as {column1: value1, column2: value2,...}
            for (k,v) in row.items():  # go over each column name and value 
                columns[k].append(v)   # append the value into the appropriate list
                                       # based on column name k
    f.close()

    #Take CSV files and convert into dict in this format...
    #
    #Dict1 = {Date1:{item1:qty1, item2:qty3, item3:qty1}
    #         Date2:{item2:qty1, item3:qty2, item4:qty1} 
    #          ...     }
    

    # Reith -- set count = 0 nd removed -1 in for loop to fic indexing missing first element of columns
    count = 0
    for x in range(len(columns['SLS_DTE_NBR'])):
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
# Create dict to represent keys to their product name
    
    prod_keys = list()
   

    with open(argv[2], "r") as f:
        reader = csv.reader(f)
        for row in reader:             # read a row as {column1: value1, column2: value2,...}
            prod_keys.append(row)
    prod_keys = prod_keys[1:]
    prod_keys = dict(prod_keys)

##################
# convert dict to counters based on months. Each month counter will contains the products sold and their count

    #print Dict1
    #sorteddict = sorted(Dict1.items(), key=operator.itemgetter(0))
    #print sorteddict

    Jan = Counter()
    Feb = Counter()
    Mar = Counter()
    Apr = Counter()
    May = Counter()
    Jun = Counter()
    Jul = Counter()
    Aug = Counter()
    Sep = Counter()
    Ocb = Counter()
    Nov = Counter()
    Dec = Counter()
    
    def which_month(date,prod_data):
        switcher ={
        
            1: lambda: Jan.update(Counter(prod_data)),
            2: lambda: Feb.update(Counter(prod_data)),
            3: lambda: Mar.update(Counter(prod_data)),
            4: lambda: Apr.update(Counter(prod_data)),
            5: lambda: May.update(Counter(prod_data)),
            6: lambda: Jun.update(Counter(prod_data)),
            7: lambda: Jul.update(Counter(prod_data)),
            8: lambda: Aug.update(Counter(prod_data)),
            9: lambda: Sep.update(Counter(prod_data)),
            10: lambda: Ocb.update(Counter(prod_data)),
            11: lambda: Nov.update(Counter(prod_data)),
            12: lambda: Dec.update(Counter(prod_data))
        }
       # Get the function from switcher dictionary
        func = switcher.get(date)
        func()
    

    # creates a date object out of the keys in Dict1
    # then which_month uses a dict to sort data by month and append into the proper counter
    for date,prod_data in Dict1.items():
        theDate = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:8]))
        which_month(theDate.month,prod_data)

#################



    # function requires a list of tuples to find product name using the product key
    # inside the prod_keys dictionary.
    # The easiest way to get a list of tuples is to pass in the output
    # from the most_common() used on a Counter collection

    def convert_id_to_name(month_counter,count_tot):
        temp = []
        for key in month_counter:
            temp.append( [prod_keys[key[0]], key[1], float(key[1])/count_tot])
        return temp
        
    MonthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    MonthData = [] 

    MonthData.append(convert_id_to_name(Jan.most_common(10), sum(Jan.values())))
    MonthData.append(convert_id_to_name(Feb.most_common(10), sum(Feb.values())))
    MonthData.append(convert_id_to_name(Mar.most_common(10), sum(Mar.values())))
    MonthData.append(convert_id_to_name(Apr.most_common(10), sum(Apr.values())))
    MonthData.append(convert_id_to_name(May.most_common(10), sum(May.values())))
    MonthData.append(convert_id_to_name(Jun.most_common(10), sum(Jun.values())))
    MonthData.append(convert_id_to_name(Jul.most_common(10), sum(Jul.values())))
    MonthData.append(convert_id_to_name(Aug.most_common(10), sum(Aug.values())))
    MonthData.append(convert_id_to_name(Ocb.most_common(10), sum(Sep.values())))
    MonthData.append(convert_id_to_name(Sep.most_common(10), sum(Ocb.values())))
    MonthData.append(convert_id_to_name(Nov.most_common(10), sum(Nov.values())))
    MonthData.append(convert_id_to_name(Dec.most_common(10), sum(Dec.values())))
    
    
    with open("Exported.csv", "w+") as f:
        writer = csv.writer(f) 
        for m_name,month_iter in zip(MonthNames, MonthData):
            writer.writerow([m_name])
            writer.writerow(["Product_Name","Total_Num_Sales","Percent_of_Months_Sales"])
  
            for lists in convert_id_to_name(Jan.most_common(10),sum(Jan.values())):
                writer.writerow(lists)
            writer.writerow([" "])

    f.close()
    
# begin gracefully
#
if __name__ == "__main__":
    main(sys.argv[0:])
#
# end of file
