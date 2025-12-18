"""
This script is a bug fix for Keysight ADS's S-Parameter Toolkit and certain vendor generated models (like PCI-SIG)
It's purpose in life is parsing Touchstone files for bad characters that ADS chokes on that aren't visible in Windows,
but it could be made to arbitrarily remove bad characters from any text file by removing some safety features
The comment lines are the offender here, so those are the lines the script acts on by splitting on the ! character
It does some rough but imperfect checking to exclude files it knows aren't Touchstone by parsing the config line
So it should be relatively safe for broad wildcard usage but isn't deeply tested for that.
"""
from sys import argv
from glob import glob
from shutil import move
from os import remove
from os import path

# Routine for input argument processing with some basic error handling for help
def inputHandler(args):
    allFiles=[]
    if len(args) > 1:
        if args[1].lower()=="help" or args[1].lower()=="-help" or args[1].lower()=="-h" or args[1].lower()=="/h":
            print("\ntstclean.py Touchstone File Cleaner Help:")
            print("Script requires an input argument from the command line")
            exit("Input arguments are filenames; lists and wildcards are both supported.")
    else:
        exit("\nError: No argument passed as input, provide input file(s) or use -help for usage info.")
    for counter in range(1,len(args)):
        allFiles += expandFiles(args[counter])
    return allFiles

# Routine to expand wildcards (if present) and return matching files in a useful list
def expandFiles(inputArgument):
    subfileList=[]
    if inputArgument.count("*"):   # If wildcard expand and find matches
        files = glob(inputArgument)
        for file in files:
            if path.isfile(file):
                subfileList.append(file)
    else:                    # Else check specific filenames against full directory listing
        files = glob("*")
        for file in files:
            if file==inputArgument:
                subfileList.append(file)
    return subfileList

# Main function for file reading and writing (handled concurrently then moved, overwriting the input file)
def main(fileList,flag="FALSE"):
    noduplicateList=[]
    for item in fileList:
        if item not in noduplicateList:
            noduplicateList.append(item)
    for touchFile in noduplicateList:
        writeFile = open("tmp1234.tmp","w")
        print ("\nOpening %s..." % touchFile)
        with open(touchFile) as readFile:
            frequencyChecker=""
            try:
                for line in readFile:
                    line = line.rstrip()   # Strip trailing whitespace and CRs, we'll put CRs back when writing
                    if line.count("#"):
                        cleanArgs=[]
                        nullCheck = line.split("#"); tsArgs = line.split(" ")
                        frequencyChecker=tsArgs[1].lower()
                        for item in tsArgs:   # This loop cleans arbitrary whitespace from Touchstone option line
                            if(item):
                                cleanArgs.append(item)
                        if len(nullCheck[0])==0 and len(cleanArgs)==6 and frequencyChecker.count("z"):
                            flag="TRUE"    # If TS option line exists with the right number of arguments, set flag
                    if line.count("!"):
                        arg = line.split("!")
                        index=0; commLine=""
                        while index < len(arg):   # Handle multiple comment characters on one line
                            if index:
                                commLine = commLine + "!" + arg[index]
                            index = index+1
                        writeFile.write(commLine +"\n")
                    else:
                        writeFile.write(line + "\n")
            except UnicodeDecodeError:    # Binary files break the script, so error handle those
                print("Error: Binary file found.")
            writeFile.close(); readFile.close()
            if flag== "TRUE":  # If identified as a Touchstone file, move temp to input otherwise delete and move on
                move("tmp1234.tmp",touchFile)
                print ("%s successfully converted." % touchFile)
                flag="FALSE"
            else:
                remove("tmp1234.tmp")
                print ("%s is not a Touchstone file and is unsupported, no modifications made." % touchFile)

# Build a file list with input arguments and wild card expansion, then act on those files
if __name__=="__main__":
    fileNames = inputHandler(argv)
    if len(fileNames):
        main (fileNames)
    else:
        exit("\nNo matching files found.")
