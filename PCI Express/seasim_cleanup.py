# This script deletes config, meas, and runlog files created by Seasim PCIe simulator that clutter model directories
# Resampled pkl touchstone files can be quite large and can eventually fill disk space, this file gets those too
# Targets specific file and folder locations for safety, doesn't do any intelligent searching for them

import os, fnmatch, time, datetime

# Function that returns a recursive list of files in directories and subdirectories
def getFileList(dirName):
    listOfFiles = os.listdir(dirName)
    allFiles = list ()
    for entry in listOfFiles:
        fullPath = os.path.join(dirName,entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getFileList(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles

# Function to handle deletion of config and meas files in TX and RX locations
def configHandle(dirName,age):
    os.chdir(dirName)
    listConfigFull = getFileList(".")
    for entry in listConfigFull:
        if(fnmatch.fnmatch(entry,'*.meas') or fnmatch.fnmatch(entry,'*.config') or fnmatch.fnmatch(entry,'*.runlog')):
            if(isFileOld(entry,age)):
                print("Deleting.... ",entry)
                os.remove(entry)
    return

# Function to check and return file age
def isFileOld(inputFile,timeInput):
    fileMod = datetime.datetime.fromtimestamp(os.path.getmtime(inputFile))
    if datetime.datetime.now() - fileMod > datetime.timedelta(hours=timeInput):
        return 1
    else:
        return 0

if(__name__=="__main__"):
    filesOlderThan = 240    # Files older than this will be deleted (in hours, 0 deletes all)
    listDirFull = getFileList(".")
    for entry in listDirFull:
        if fnmatch.fnmatch(entry,"*.pkl*"):
            if(isFileOld(entry,filesOlderThan)):
                print("Deleting.... ",entry)
                os.remove(entry)
    configHandle("..\PCIE_GEN4_TX",filesOlderThan)
    configHandle("..\PCIE_GEN4_RX",filesOlderThan)
    exit(time.sleep(5))    # Give time for non command line users to read deletions

