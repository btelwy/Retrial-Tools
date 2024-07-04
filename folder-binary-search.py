import os
import pathlib
from pprint import pprint as pprint

#high level:
#recursively search through ExtractedMaterials folder
#to find matches for inputted sequence of bytes

def strToBytes(inputStr):
    assert(len(inputStr) > 0 and len(inputStr) % 2 == 1, "Input not parsable as hex")

    parsedHex = []
    while (len(inputStr) > 0):
        nextInt = int(inputStr[0 : 2], base=16)
        parsedHex.append(nextInt)
        inputStr = inputStr[2 : ]
    
    return bytes(parsedHex)

rawInput = input("Enter sequence of hex bytes without prefixes or spaces:\n")
hexSequence = strToBytes(rawInput)

#choose the folder of binary files
folder = "C:\\Users\\ben\\Desktop\\AJ-Retrial\\ExtractedMaterials"

#the list that will contain the matching files
matches = []

#iterate through each file in the folder recursively
for (root, dirs, files) in os.walk(folder):
    for item in files:
        path = pathlib.Path(f'{root}/{item}') #get path of selected file
        absolutePath = pathlib.Path.absolute(path)

        with open(absolutePath, 'rb') as f:
            #read the entire file into a string of bytes
            fileBytes = f.read()
            offset = fileBytes.find(hexSequence) #byte offset of match in file, or -1 if none
            
            #and check that string of bytes for the byte sequence
            if (offset != -1):
                matches.append((f.name, offset))


if (len(matches) == 0): #if matches is empty
    print("No matches found.")
else:
    pprint(matches)