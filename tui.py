#!/usr/bin/env python3

import json
import os, sys

def clear():
    '''
    Clears the screen of any printed text
    '''
    os.system('cls' if os.name == 'nt' else 'clear')

def loadData(dataFile):
    '''
    Loads data from a json file into memory
    '''

    with open(dataFile, "r") as file:
        data = json.load(file)

    return data

def saveData(data, dataFile):
    '''
    Dumps data from a dictionary or array into a JSON file
    '''

    with open(dataFile, "w") as file:
        json.dump(data, file)

def printPage(choices, pageLimit = 10):
    '''
    Prints the choices available to choose from.
    Returns the key for the option picked.
    
    choices is a dictionary
    pageLimit modifies how many choices appear on the screen

    '''
    keyNames = [k for k in choices]
    numKeys = len(keyNames)

    while True:
        for i, c in enumerate(keyNames):
            if i % pageLimit == 0:
                clear()
                lower = 0 if i < pageLimit else pageLimit * ((i // pageLimit) - 1)
                print("Pick the option you desire from the choices available.")
                print("Type '>' to go to the next page or '^' to go up one level")
                print("Type 'q' to quit, 's' to save the current structure, and 'r' to return the current structure.\n")
            
            if isinstance(choices[c], list) or isinstance(choices[c], dict):
                printData = type(choices[c])
            else:
                printData = choices[c]

            print(f"\t {i}) {c} : {printData}")

            if (i + 1) % pageLimit == 0 or numKeys - 1 == i:
                upper = i
                print(f"\nOptions {lower} - {upper}")
                choice = input('--> ')
                while choice != '>':
                    if choice.isnumeric() and int(choice) < len(keyNames):
                        return keyNames[int(choice)]
                    elif choice == 'q':
                        return 0
                    elif choice == 's':
                        saveData(choices, "data.json")
                        choice = input("Current Choice Saved. --> ")
                    elif choice == 'r':
                        print("Returning current data structure")
                        return 0
                    elif choice == '^':
                        return 1

                    else:
                        choice = input('Invalid Input. Numbers or ">" only. --> ')
                
    raise Exception("How did you get here?")

def browseData(data):
    '''
    Builds a TUI to browse data from a JSON format
    Eventually returns the data found
    '''
    if isinstance(data, dict):
        choices = data
    elif isinstance(data, list):
        choices = {f"Option {i}" : d for i, d in enumerate(data)}
    else:
        clear()
        print(f"Data: {data}")
        return data

    option = printPage(choices)
    if option == 0:
        print("Thanks for using me!")
        return data # Returns the data structure we ended up at
    elif option == 1:
        return None

    value = browseData(choices[option])

    if value is not None:
        return value

    return browseData(choices)
    

if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        dataFile = args[1]
    else:
        dataFile = 'data.json'
    data = loadData(dataFile)
    browseData(data)
