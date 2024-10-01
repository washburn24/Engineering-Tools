"""
This script is a bug fix for Keysight ADS's S-Parameter Toolkit and certain vendor generated models (like PCI-SIG)
It's purpose in life is parsing Touchstone files for bad characters that ADS chokes on that aren't visible in Windows,
but it could be made to arbitrarily remove bad characters from any text file by removing some safety features
The comment lines are the offender here, so those are the lines the script acts on by splitting on the ! character
It does some rough but imperfect checking to exclude files it knows aren't Touchstone by parsing the config line
So, it should be relatively safe, but it's only really tested on .sNp files.
"""
from sys import argv
from glob import glob
from shutil import move
from os import remove
from os import path

# Routine to expand wildcards (if present) and return matching files in a useful list
def expandFiles(inFile):
    fileList=[]
    if(inFile.count("*")):   # Expand wildcard and find matches
        files = glob(inFile)
        for file in files:
            if(path.isfile(file)):
                fileList.append(file)
    else:                    # Or check filenames against full directory listing
        files = glob("*.*")
        for file in files:
            if(file==inFile):
                fileList.append(inFile)
    return(fileList)

# Main function for file reading and writing (handled concurrently then moved, overwriting the input file)
def main(fileList,token):
    for inFile in fileList:
        tempFile = open("tmp1234.tmp","w")
        print ("\nOpening %s..." % inFile)
        with open(inFile) as readFile:
            try:
                for line in readFile:      # Read input file a line at a time until we have all lines
                    line = line.rstrip()   # Strip trailing whitespace and CRs
                    if(line.count("#")):
                        cleanArgs=[]
                        nullCheck = line.split("#"); tsArgs = line.split(" ")
                        freqCheck=tsArgs[1].lower()
                        for item in tsArgs:   # This loop cleans arbitrary whitespace from option line
                            if(item):
                                cleanArgs.append(item)
                        if(len(nullCheck[0])==0 and len(cleanArgs)==6 and freqCheck.count("z")):
                            token=7    # If TS option line exists with the right number of arguments, set token
                            freqCheck=""
                    if(line.count("!")):
                        arg = line.split("!")  # Split on comment character to check for bad lines
                        index=0; commLine=""
                        while (index < len(arg)):   # Handle multiple comment characters on one line
                            if(index):
                                commLine = commLine + "!" + arg[index]
                            index = index+1
                        tempFile.write(commLine +"\n")
                    else:
                        tempFile.write(line + "\n")
            except UnicodeDecodeError:    # Binary files break the script, so check for those
                pass    # Don't act on the error, the main loop will clean things up and go to next file
            tempFile.close(); readFile.close()
            if(token==7):    # If identified as a Touchstone file, move temp to input otherwise delete and do nothing
                move("tmp1234.tmp",inFile)
                print ("%s successfully converted." % inFile)
                token=0
            else:
                remove("tmp1234.tmp")
                print ("%s is not a Touchstone file and is unsupported, no modifications made." % inFile)

if __name__=="__main__":
    AllFiles=[]
    # Input argument processing with some basic error handling and disaster avoidance via exit conditions
    if(len(argv) > 1):
        if(argv[1].lower()=="help" or argv[1]=="--help" or argv[1]=="-h" or argv[1]=="/h"):
            print("\ntstclean.py Touchstone Cleaner Help:")
            print("Script requires an input argument from the command line")
            exit("Input arguments are filenames, lists and wildcards are both supported.")
        for counter in range(1,len(argv)):
            AllFiles = AllFiles + expandFiles(argv[counter])
    else:
        exit("\nError: No argument passed as input, provide input file(s) or use -h for help.")
    # Once a valid file list is assembled process them in main function, if none found exit
    if(len(AllFiles)):
        main (AllFiles,0)
    else:
        exit("\nNo matching files found.")
