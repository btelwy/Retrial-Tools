import os
import pathlib
from pprint import pprint as pprint

#high level:
#recursively search through ExtractedMaterials folder
#to find matches for inputted sequence of bytes

def convertStrToBytes(inputStr):
    assert(len(inputStr) > 0 and len(inputStr) % 2 == 0)

    parsedHex = []
    while (len(inputStr) > 0): #repeatedly process then remove first two characters of string
        nextInt = int(inputStr[0 : 2], base=16)
        parsedHex.append(nextInt)
        inputStr = inputStr[2: ]
    
    return bytes(parsedHex)


def searchFolder(folder):
    matches = []

    for (root, _, files) in os.walk(folder): #iterate through each file in the folder recursively
        for item in files:
            path = pathlib.Path(f'{root}/{item}') #get path of selected file
            absolutePath = pathlib.Path.absolute(path)

            with open(absolutePath, 'rb') as f:
                fileBytes = f.read()
                offset = fileBytes.find(hexSequence) #byte offset of match in file, or -1 if none
                
                if (offset != -1): #and check that string of bytes for the byte sequence
                    matches.append((f.name, offset))
    
    return matches



rawInput = input("Enter sequence of hex bytes without prefixes or spaces:\n")
hexSequence = convertStrToBytes(rawInput)

#The filepath to the AJ-Retrial folder must be C:\Users\[username]\Desktop\
username = input("Enter your username on your computer:")
folder = f"C:\\Users\\{username}\\Desktop\\AJ-Retrial\\ExtractedMaterials"

matches = searchFolder(folder)

if (len(matches) == 0):
    print("No matches found.")
else:
    pprint(matches)