"""
This script coverts Cadence Allegro Pin Delay exports from English to Metric units. It started from another script so
it does stuff you shouldn't really need like wildcard expansion. We won't modify the input file but rather generate
files with the same basename appended with _metric. This makes double checking the results in constraint manager
easier on the back end, saving you mental conversion. If an output target exists it is overwritten so this script is
safe to run multiple times. It also checks for MIL in the input file, so wildcards are safe on already converted files.
"""
from sys import argv
from glob import glob
from os import remove, path

# Routine for input argument processing with some basic error handling for help
def inputHandler(args):
    allFiles=[]
    if(len(args) > 1):
        if(args[1].lower()=="help" or args[1].lower()=="-help" or args[1].lower()=="-h" or args[1].lower()=="/h"):
            print("\npindelay.py Allegro English to Metric Unit Conversion Help:")
            print("Script requires an input argument from the command line")
            exit("Input arguments are filenames; lists and wildcards are both supported.")
        for counter in range(1,len(args)):
            allFiles = allFiles + expandFiles(args[counter])
    else:
        exit("\nError: No argument passed as input, provide input file(s) or use -help for usage info.")
    return(allFiles)

# Routine to expand wildcards (if present) and return matching files in a useful list
def expandFiles(inputArgument):
    subfileList=[]
    if(inputArgument.count("*")):   # If wildcard expand and find matches
        files = glob(inputArgument)
        for file in files:
            if(path.isfile(file)):
                subfileList.append(file)
    else:                    # Else check specific filenames against full directory listing
        files = glob("*")
        for file in files:
            if(file==inputArgument):
                subfileList.append(file)
    return(subfileList)

# Main function for file reading and writing (handled concurrently)
def main(fileList,flag="FALSE"):
    noduplicateList=[]
    for item in fileList:
        if item not in noduplicateList:
            noduplicateList.append(item)
    for inputFile in noduplicateList:
        if inputFile.count("."):  # Build output filename but support files that don't have a "."
            outputFile = inputFile.split(".")[0] + "_metric." + inputFile.split(".")[1]
        else:
            outputFile = inputFile + "_metric"
        outFile = open(outputFile,"w")
        print ("\nOpening %s..." % inputFile)
        with open(inputFile) as readFile:
            try:
                for line in readFile:
                    line = line.rstrip()   # Strip trailing whitespace and CRs, we'll put CRs back when writing
                    if(line.count("MIL")):
                        flag = "TRUE"
                        pinName = line.split(",")[0]
                        lengthEnglish = line.split(",")[1]
                        lengthEnglish = lengthEnglish.split(" ")[0]
                        lengthMetric = round(float(lengthEnglish) / 39.37,4)  # Rounding to 4 decimal places like Allegro
                        outFile.write(pinName + "," + str(lengthMetric) + " MM" + "\n")
                    else:
                        outFile.write(line + "\n")
            except UnicodeDecodeError:    # Binary files break the script, so check for those
                print("Error: Binary file found.")
            outFile.close(); readFile.close()
            if(flag=="TRUE"):
                print (inputFile + "successfully converted to " + outputFile); flag="FALSE"
            else:
                print ("No English units found in input file " + inputFile + ". Nothing to do."); remove(outputFile)

# Build file list with input arguments and wild card expansion, then act on those files
if __name__=="__main__":
    fileNames = inputHandler(argv)
    if(len(fileNames)):
        main (fileNames)
    else:
        exit("\nNo matching files found.\n")
