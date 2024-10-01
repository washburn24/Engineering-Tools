"""
The purpose of this script is to call HSpice from the command line while gracefully handling license errors.
It assumes one total available license as implmented here.  It's purpose in life is to keep long batch
simulations with lots of HSPice runs from crashing.  You need LMTools installed for the license checking to
work.  It supports drag and drop and Send To menu usage also, depending on workflow.

Usage: Call the script with 'hsp_runner.py' in place of 'hspice' with normal HSpice syntax.  All command line
switches that are available in HSpice are supported, though -i, -o, -mt are all that are heavily tested.
The -d switch is automatically invoked to keep console output brief and useful for the user.  This
script pops a process out of the command window because 2009.09 and higher don't print status properly during
simulation, which provides the appearance of a hang during long simulation runs.
"""
from sys import argv
from time import sleep
from subprocess import call
import os, fileinput

# Check license server for available license (crude...assumes one license total)
def checkLicense(inUse):
    while(inUse):
        count = 0
        licStat = os.popen("lmutil lmstat -a -c 27008@LICENSE_SERVER")
        for line in licStat:
            if(line.count("\"hspice\"")): # "hspice" shows up when license in use
                count = count + 1
        if(count==1):
            if(inUse==2):
                print ("\nHSpice License in use, waiting.",)
            inUse=1
            for i in range(0,9):       # Patiently wait for license to free
                sleep(1)
                if(i%3==0): print ("\b.",)
        else:
            inUse=0

# Function to handle the specifics of the HSpice command line call
def main():
    inFile=""; outFile=""; statFile=""; argString=""; outFlag=1
    try:
        inFile = argv[1]
    except IndexError:      # If no arguments, print hspice help and exit
        exit(os.system("hspice"))
    for i in range(1,len(argv)):
        if(argv[i]=="-o"):               # Check for output file switch
            outFlag = 0
            try:
                outFile = argv[i+1]
            except IndexError:
                exit("\nNo output file supplied after %s switch" % argv[i])
        if(argv[i]=="-i"):               # Check for input file switch
            try:
                inFile = argv[i+1]
            except IndexError:
                exit("\nNo input file supplied after %s switch" % argv[i])
        argString = argString + argv[i] + " " # Concat command line arguments

    if(outFlag):           # Fixes weird behavior in 2010 if -o isn't used
        outFile = os.path.splitext(inFile)[0] + ".lis"
        argString = argString + "-o " + outFile
    statSplit = outFile.split(".")
    if(statSplit[len(statSplit)-1]=="lis"):
        statSplit.pop()
    for j in range(0,len(statSplit)):   # Construct the .st0 filename
        statFile = statFile + statSplit[j] + "."
    statFile = statFile + "st0"
    if(os.path.isfile(statFile)):
        os.remove(statFile)             # Erase the existing .st0 file

    if(os.path.isfile(inFile)):
        checkLicense(2)
        while(1):
            try:
                call("hspice %s -d" % argString)  # -d invoked automatically
            except WindowsError:   # Die gracefully when hspice isn't in Path
                print ("\nError! Can't find hspice.exe in your Path!")
                exit(sleep(4))      # Give drag/drop users time to read error
            if(os.path.isfile(statFile)):
                for line in fileinput.input(statFile):
                    print (line.strip())  # Print status after popup closes
                fileinput.close()
                break        # Break retry loop when .st0 file is found
    else:
        exit("\nInput file not found!")

if(__name__=="__main__"):
    main()

