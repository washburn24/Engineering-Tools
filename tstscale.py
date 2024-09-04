"""
This script scales Touchstone S-parameter data according to specific equations
to build variable loss simulations out of fixed vendor models or datasets
"""
import math
from os import path
from fileinput import input
from sys import argv
from glob import glob

def magHandle(arg):
    magScaler = 1.5   # Modify the magnitude scale here
    return(str(float(arg)*float(magScaler))

def freqHandle(arg):
    freqScaler = 1.0   # Modify the frequency scale here
    return(str(float(arg)*float(freqScaler)))

# Routine to open input file, scale data, and write output file
def scaleFile(inFile):
    dataList=[]
    for line in input(inFile):
        if(line.count("!")):      # Do nothing with commented lines
            dataList.append(line)
        elif(line.count("#")):    # This line defines type of data in file
            dataList.append("!Data scaled by parsing utility. Use carefully.\n")
            dataList.append(line)
            dataType = line.split()
            if(dataType[2]!="S" or dataType[3]!="dB"):
                print ("\nWarning! Data type not yet supported.")
                return("Error")  # Error if the file's datatype isn't what we assume
        else:
            numArray=[]; flag=0; tempStr=""
            data=line.split()
            if(len(data)==8):
                for arg in data:
                    numArray.append(magHandle(arg))
            if(len(data)==9):
                numArray.append(freqHandle(data[0]))
                for i in range(1,9):
                    numArray.append(magHandle(data[i]))
            for num in numArray:
                tempStr=tempStr + num + " "
                flag=1
            if(flag):
                dataList.append(tempStr+"\n")
                flag=0
    fileOut=open("scaled."+inFile,'w')    # Write the modified data to a new file
    for stuff in dataList:
        fileOut.write(stuff)

# Routine to expand wildcards (if present) and return useful list of files
def expandFiles(inArgs):
    fileList=[]
    for i in range(1,len(inArgs)):
        if(inArgs[i].count("*")):      # Expand wild cards in command line input
            files = glob(inArgs[i])
            if(len(files)==0):
                print ("No files match %s" % inArgs[i])
            for file in files:
                fileList.append(file)
        else:
            fileList.append(inArgs[i])
    return(fileList)

fileList = expandFiles(argv)
for file in fileList:
    if(path.isfile(file)):     # Make sure the file exists to avoid crashing
        errCheck = scaleFile(file)
        if(errCheck!="Error"):
            print ("File %s converted" % file)
    else:
        print ("%s not found" % file)
