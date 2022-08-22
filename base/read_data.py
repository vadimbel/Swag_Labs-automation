
import csv

"""
    This file contains a method created to use ddt and read values from csv file from 'csv_files' package
"""

def getCSVData(fileName):
    # create an empty list to store rows
    rows = []
    # open the CSV file
    dataFile = open(fileName, "r")
    # create a CSV Reader from CSV file
    reader = csv.reader(dataFile)
    # skip the headers
    next(reader)
    # add rows from reader to list
    for row in reader:
        rows.append(row)

    return rows
