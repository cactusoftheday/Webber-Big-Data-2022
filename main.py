# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import csv
import os
import numpy as np
from apyori import apriori
import pandas as pd
from pprint import pprint

def readfile(fileName):
    with open(fileName, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        csvArray = []
        temp = []
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                for i in range(0, len(row)):
                    temp.append(row[i])
                line_count += 1
            else:
                for i in range(0, len(row)):
                    temp.append(row[i])
                    #print({row[i]}, end = " ")
                #print()

                line_count += 1
            csvArray.append(temp[:])
            temp.clear()
        #print(f'Processed {line_count} lines.')

    csvArray = np.array(csvArray,dtype=object)
    return csvArray

def apSubjectCount(csvArray):
    columnAP = 11
    apSubjects = ["AP Chemistry","AP English","AP Biology","AP Physics","AP Math","AP GH","AP Art/Drama","AP Spanish","AP French","AP Mandarin","AP Programming","no AP"]

    for i in range(0,len(apSubjects)):
        tempColumn = []
        subject = apSubjects[i]
        for row in csvArray:
            if("Timestamp" in row):
                continue
            if(subject[3:] in row[4]):
                #print("yes")
                tempColumn.append(["Takes " + subject])
            else:
                tempColumn.append(["Doesn't take " + subject])
        print(len(tempColumn))
        print(len(csvArray))
        csvArray = np.append(csvArray,tempColumn,axis=1)
    return csvArray

def foodSorter(csvArray):
    for row in csvArray:
        for i in range(0,len(row)):
            if(i == 3):
                temp = row[i].lower()
                if('pasta' in temp):
                    row[i] = 'baked pasta'
                elif('butter chicken' in temp):
                    row[i] = 'butter chicken'
                elif('bbq' in temp or 'barbeque' in temp):
                    row[i] = 'bbq chicken'
                elif('burger' in temp):
                    row[i] = 'burger'
                elif('souvlaki' in temp or 'greek' in temp):
                    row[i] = 'souvlaki'
                elif('teriyaki' in temp):
                    row[i] = 'chicken teriyaki'
                elif('chili' in temp):
                    row[i] = 'chili'
                elif('dumpling' in temp):
                    row[i] = 'dumpling'
                elif('pizza' in temp):
                    row[i] = 'pizza'
                elif('pork' in temp and 'dumpling' not in temp):
                    row[i] = 'pork tenderloin'
                elif('taco' in temp):
                    row[i] = 'taco'
    return csvArray

def readfileWithPandas(fileName):
    dataset = pd.read_csv(fileName, header=1)
    dataset.shape

    csvArray = []
    for i in range(0, dataset.shape[0]):
        csvArray.append([str(dataset.values[i,j]) for j in range(0,11)])
    return csvArray

if __name__ == '__main__':
    csvArray = readfileWithPandas("cleaned.csv")
    #print(csvArray)
    csvArray = apSubjectCount(csvArray)

    '''funni = [["apple", "orange"],["apple","banana","orange"],["apple", "banana","orange"]]
    rules = apriori(funni,min_support=0.5,min_length = 3)
    for rule in rules:
        print(rule)'''

    rules = apriori(csvArray,min_support = 0.4, min_length = 2, max_length=2)
    results = list(rules)
    results = pd.DataFrame(results)
    items = results["items"]
    items = [list(x) for x in items]
    print(items)
    for i in range(0, len(items)):
        current_item = items[i]
        if(len(current_item) == 1):
            current_item.append("")
        current_item[0].replace("\"","")
        current_item[1].replace("\"", "")
        items[i] = current_item
    support = results["support"]
    support = [y for y in support]
    print(support)
    rows = []
    if(len(items) != len(support)):
        raise Exception("Oops the lists are not of the right length!")
    for i in range(0,len(items)):
        rows.append([i,items[i][0],items[i][1],support[i]])
    file = open("support2.csv", "w+", newline='')
    with file:
        write = csv.writer(file)
        write.writerows(rows)


    '''for result in results:
        print(result)'''


