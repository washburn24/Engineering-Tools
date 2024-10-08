"""
Script to move the .png images created by SigTest to a subdirectory for less clutter
Only tested with SigTest 3.1.9 and makes some assumptions about how it makes files
"""
import glob, fileinput, os
from shutil import move
from sys import argv

def processFiles(inArg,subdirName):
    for file in glob.glob(inArg):
        outFile = open("temp.temp","w")
        if(file.count(".htm")):    # Crudely restrict processing to only HTML files
            for line in fileinput.input(file):
                imgArg = line.split(".png")[1].split("src=")
                if(imgArg[1].count("\\")==1): # Paths with exactly one \ need modified
                    line = line.replace("=\".","=\".\\%s" % subdirName)
            outFile.write(line)
            outFile.close()
            move("temp.temp",file)

    if(os.path.isdir(subdirName)==0):      # If the directory doesn't exist, make it
        os.mkdir(subdirName)

    inArg = inArg.split(".")[0] + "*Eye.png"
    for file in glob.glob(inArg):          # Moves appropriate .png files
        move(file,os.path.join(subdirName,file))

if(__name__=="__main__"):
    if (len(argv) != 3):
        exit("\nError! Usage: 'sigtest_clean.py *.html subdirectory'")
    else:
        processFiles(argv[1],argv[2])
    print ("Done!")
