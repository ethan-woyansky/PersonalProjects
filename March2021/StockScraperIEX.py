###Scrape financial statements using IEX Cloud API and make them into tabular .csv files
###All financial data provided by IEX Cloud: https://iexcloud.io/

import requests #API Request support
import os.path #Modification of file directory for saving files
import csv #Create .csv file output
import pandas as pd #Dataframe support
import string #.format()
import tkinter as tk #GUI Support
from tkinter import filedialog

###Define reference dictionaries that relate to inputs for variable outputs
timeDict = { #Defines whether the query is for Annual Data or Quarterly Data.
    'A': 'annual',
    'Q': 'quarter'
}

seriesDict = { #Financial statement choices
    1: 'balance-sheet', 
    2: 'income', 
    3: 'cash-flow'
}

rangeDict = { #Defines the time range for historical price queries
    1: 'max',
    2: '5y',
    3: '2y',
    4: '1y',
    5: 'ytd',
    6: '6m',
    7: '3m',
    8: '1m',
    9: '1mm',
    10: '5d',
    11: '5dm',
    12: 'dynamic'
}

###Function that creates a list from a space separated input
###Returns a list of stock tickers
def createEquityList():
    while True:
        print("> Please enter a list of equities, separated by spaces.")
        equities = str(input())
        if all(x.isalpha() or x.isspace() for x in equities): #Do not want special characters (note to self: this excludes BRK.B type names)
            break
        else:
            print("> Invalid character(s) entered.\n")
            continue

    equities = equities.upper() #Capitalize tickers for syntax and stylistic intent
    equityList = equities.split() #Creates the list from the string, separated by whitespace
    return equityList

###Define the parameters for the overall data request
###Returns a list of two values for index keys
def defineDataRequest():
    generalChoices = list(range(1,5)) 
    seriesChoices = list(range(1,13))
    timeChoices = ['A', 'Q']
    
    print("\n---Define Parameters---")
    while True:
        print("> Please define the source from which you want to chart your information.")
        print(">  | '1': Balance Sheet | '2': Income Statement | '3': Cash Flow Statement | '4': Price History")
        seriesType = int(input())
        
        if seriesType not in generalChoices:
            print("> Not a valid choice.")
            continue
        
        if seriesType != 4:
            print("\n---Define Series---")
            print("> Please choose between annual and quarterly financial statements.")
            print("> 'A': Annual | 'Q': Quarterly")
            timeType = str(input()).upper()
            
            if timeType not in timeChoices:
                print("> Not a valid choice.")
                continue
        
        elif seriesType == 4:
            print("\n---Please select your price range: (Type a number)---\n")
            print("______________")
            
            for key, value in rangeDict.items():
                key = str(key)
                print("{:<4} | {:>7}".format(key, value))
            timeType = f"\n> {int(input())}"
            
            if timeType not in seriesChoices:
                print("> Not a valid choice.")
                continue
        break

    finalList = [seriesType, timeType]
    return finalList

###Query information from the IEXCloud API
def grabInformation():
    print("\n---Requesting Financial Information---")
    
    equityList = createEquityList() #Calling equityList to generate a list of equities.
    finalList = defineDataRequest() #Calling finalList to generate index keys for variable evaluation
    f_num = 0 #The number of files that will be generated.
    
    print("\n> Please enter the directory for your files.\n")
    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askdirectory(title='Select Folder') #Using Tkinter to have the user specify their file directory. Each file for the remainder of this function call will be placed there.
    print(f"\nFile Directory: {filepath}") #Specifying the filepath to the user
    
    for equity in equityList: #Loop through the API Query for each stock listed returned from createEquityList()
        
        if finalList[0] != 4: #The first check references Balance Sheets, Income Statements and Cash Flow Statements. Need to do this way due to the API parameters
            
            parameters = {
                'period': f'{timeDict[finalList[1]]}',
                'last': 4 #This always returns the last 4 entries of the request (e.g. Last 4 years for annual reports, last 4 quarters for quarterly reports)
            }
            
            r = requests.get(f'https://cloud.iexapis.com/stable/stock/{equity}/{seriesDict[finalList[0]]}?token=pk_36c9ff694f3642a3bc843467e7e6cc5e', params=parameters)
            data = r.json() #Save the api request to a .JSON file for parsing
            
            if seriesDict[finalList[0]] == 'balance-sheet': #Key to open the inner dictionary
                sheetInfo = data[f'balancesheet']
            elif seriesDict[finalList[0]] == 'income':
                sheetInfo = data[f'income']
            elif seriesDict[finalList[0]] == 'cash-flow':
                sheetInfo = data[f'cashflow']
            
            myFrame = pd.DataFrame(sheetInfo) #Create a dataframe using pandas for export format.   
            myFrame.set_index('fiscalDate', inplace=True) #Setting the leftmost column of the dataframe to be the date values.
            myFrame = myFrame.T  #Transpose the dataframe for better excel formatting
            filename = f"{equity}_{seriesDict[finalList[0]]}_{timeDict[finalList[1]]}" #Create filename using our established variables
        
        elif finalList[0] == 4: #The second check references lists of prices. 
            
            parameters = {
                'range': f'{rangeDict[finalList[1]]}'
            }

            r = requests.get(f'https://cloud.iexapis.com/stable/stock/{equity}/chart?token=pk_36c9ff694f3642a3bc843467e7e6cc5e', params=parameters)
            data = r.json()
            myFrame = pd.DataFrame(data)
            myFrame.set_index('date', inplace=True) #Setting the leftmost column of the dataframe to be the date values.
            filename = f"{equity}_PRICES_{rangeDict[finalList[1]].upper()}"
        
        completename = os.path.join(filepath, filename+'.csv')
        myFrame.to_csv(completename) #Export the file to the filepath (completename) in .csv format
        f_num += 1 #Add 1 to the number of files created.
    
    print(f"\n---Request Completed---") 
    print(f"{f_num} file(s) created in {filepath}") #Specifies number of files written to the user.

grabInformation() #Run