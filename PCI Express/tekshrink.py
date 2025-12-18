"""
This script strips unneeded data out of a Tek scope output file to reduce
file size and processing time in SigTest (tested with .csv and .txt only)
"""
from os import path
from fileinput import input
from sys import argv
from glob import glob
from shutil import move

# Routine to open, shrink, and rewrite each passed file
def shrinkFile(inFile):
    fileOut=open("temp123.temp",'w')
    for line in input(inFile):
        arg = line.split(",")
        if len(line) and arg.count(";"):  # If data exists and uncommented
            arg = float(arg.pop().strip())
            fileOut.write(str(arg)+'\n')
        else:       # If the first element not empty, it's header info
            fileOut.write(line)
    fileOut.close()
    move("temp123.temp",inFile)

if __name__== "__main__":
    fileList=[]
    for i in range(1,len(argv)):
        if argv[i].count("*"):      # Expand wild cards in command line input
            files = glob(argv[i])
            if len(files)==0:
                print ("No files match %s" % argv[i])
            for file in files:
                fileList.append(file)
        else:
            fileList.append(argv[i])

    for file in fileList:
        if path.isfile(file):     # Make sure the file exists to avoid crashing
            shrinkFile(file)
            print ("File %s converted" % file)
        else:
            print ("%s not found" % file)

