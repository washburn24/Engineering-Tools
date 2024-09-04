"""
This script coverts Cadence Allegro Pin Delay exports from English to Metric units.  It's started from another
script so it does stuff you shouldn't really need like wildcard expansion.  We won't modify the input file but
rather generate files with the same basename appended with _metric.  This makes double checking the results in
constraint manager easier on the back end but this conversion. If an output target exists it is overwritten so
this script is safe to run multiple times.
"""
from sys import argv
from glob import glob
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

# Main function for file reading and writing (handled concurrently)
def main(fileList,token):
    for inFile in fileList:
        token = 0
        if inFile.count("."):  # Build output filename but support files that don't have a "."
            outName = inFile.split(".")[0] + "_metric." + inFile.split(".")[1]
        else:
            outName = inFile + "_metric"
        outFile = open(outName,"w")
        print ("\nOpening %s..." % inFile)
        with open(inFile) as readFile:
            try:
                for line in readFile:      # Read input file a line at a time until we have all lines
                    line = line.rstrip()   # Strip trailing whitespace and CRs
                    if(line.count("MIL")):
                        token = 7
                        pinName = line.split(",")[0]
                        lengthEnglish = line.split(",")[1]
                        lengthEnglish = lengthEnglish.split(" ")[0]
                        lengthMetric = round(float(lengthEnglish) / 39.37,4)  # Rounding to 4 decimal places like Allegro
                        outFile.write(pinName + "," + str(lengthMetric) + " MM" + "\n")
                    else:
                        outFile.write(line + "\n")
            except UnicodeDecodeError:    # Binary files break the script, so check for those
                remove(outName)  # If we choke on a binary, the outfile should be deleted
            outFile.close(); readFile.close()
            if(token==7):
                print (inFile + "successfully converted to " + outName)
                token=0
            else:
                remove(outName)
                print ("No English units found in input file " + inFile + ". Nothing to do.")

if __name__=="__main__":
    AllFiles=[]
    # Input argument processing with some basic error handling and disaster avoidance via exit conditions
    if(len(argv) > 1):
        if(argv[1].lower()=="help" or argv[1].lower()=="--help" or argv[1]=="-h" or argv[1]=="/h"):
            print("\nPinDelay.py Help:")
            print("Script requires an input argument from the command line")
            exit("Input arguments are filenames, lists and wildcards are both supported.")
        for counter in range(1,len(argv)):
            AllFiles = AllFiles + expandFiles(argv[counter])
    else:
        exit("\nError: No argument passed as input, provide input file(s) or use -h for help.\n")
    # Once a valid file list is assembled process them in main function, if none found exit
    if(len(AllFiles)):
        main (AllFiles,0)
    else:
        exit("\nNo matching files found.\n")
