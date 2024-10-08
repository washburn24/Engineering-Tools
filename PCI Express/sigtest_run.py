"""
This script batches SigTest with support for Dual Port mode.  That mode is explicit and expects
file format is something_data.wfm and something_clk.wfm but .csv files are also supported.
Only differential files tested so far.
Make sure SigTest is in your Path...this script won't go find it.
"""
from glob import glob
from sys import argv
import os

# Set user defined stuff here
sampleInt = "20"                            # Set sample interval (in ps)
templateFile = "\pcie_2_0_card\TX_ADD_CON_6.0DB.dat"  # Set template file
safeMode = "False"       # Turn on safe mode "True" (script will print commands but not run them)

# Routine to expand wildcards (if present) and return useful list of files
def expandFiles(inFile):
    fileList=[]
    if(inFile.count("*")):
        files = glob(os.path.join(inFile))
        for file in files:
            fileList.append(file)
    else:
        files = glob(os.path.join("*.*"))
        for file in files:
            if(file==inFile):
                fileList.append(inFile)
    return(fileList)

# The meat of the stuff in this script is here
def processFiles(inFiles):
    global sampleInt
    global templateFile
    global safeMode
    datFiles=[]; clkFiles=[]
    inFiles = expandFiles(inFiles)
    if(templateFile.count("DUAL_PORT")):  # If "DUAL_PORT" is in the template name, do this
        for arg in inFiles:
            if(arg.count("data")):       # Assumes a tag in the data waveform filename
                datFiles.append(arg)
            elif(arg.count("clk")):      # Assumes a tag in the clock waveform filename
                clkFiles.append(arg)
        for datArg in datFiles:
            datToken = datArg.split("data")   # Split on "data" to match the clk filename
            for clkArg in clkFiles:
                if(clkArg.count(datToken[0])):   # Build the command line with arguments
                    commandArg = "SigTest /d %s" % os.getcwd()
                    commandArg = commandArg + " /si %s " % sampleInt
                    commandArg = commandArg + "/t %s" % templateFile
                    commandArg = commandArg +" /s %s " % datArg + "/cs %s " % clkArg
                    if(safeMode.lower() == "true"):
                        print (commandArg)
                    else:
                        print ("Running SigTest on %s" % datArg)
                        os.system(commandArg)
    else:         # If this isn't a dual port test, do this (this mimics the old .bat file)
        for arg in inFiles:                # Build the command line with arguments
            commandArg = "SigTest /d %s" % os.getcwd()
            commandArg = commandArg + " /si %s " % sampleInt
            commandArg = commandArg + " /t %s" % templateFile
            commandArg = commandArg + " /s %s " % arg
            if(safeMode.lower() == "true"):
                print (commandArg)
            else:
                print ("Running SigTest on %s" % arg)
                os.system(commandArg)

if(__name__=="__main__"):
    if(len(argv) < 2):      # Accept exactly one argument (data filename wildcard)
        exit("No arguments given for SigTest to process. Exiting.")
    elif(len(argv) > 2):
        exit("Too many arguments given. Exiting.")
    else:
        processFiles(argv[1])
