#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
from subprocess import check_output,call
from datetime import datetime
import fileinput 

# find the logs directory
curDir = os.path.dirname(os.path.realpath(__file__))
logDir = os.path.join(curDir,'logs')
os.makedirs(logDir, exist_ok=True) # in case it doesn't exist
now = datetime.now()
logPath = os.path.join(logDir,now.strftime("%Y-%m-%d") + "_log.md")

try:
    # bulk of code (should be its own file, while the rest of this code is a generic wrapper for any script)
    # --------------------
    pathToMainDrive = ""
    pathToBackup = ""
    maxDiff = 30 # gigabytes

    # make sure both directories have trailing slashes
    if not (pathToMainDrive.endswith("/") and pathToBackup.endswith("/")):
        raise Exception("drive paths must have trailing slashes")

    # check that both drives are a mount point
    if not os.path.ismount(pathToMainDrive):
        raise Exception(pathToMainDrive + " is not a mountpoint")
    if not os.path.ismount(pathToBackup):
        raise Exception(pathToBackup + " is not a mountpoint")
        
    # check that contents of both drives are within X GB of eachother
    stats_main = os.statvfs(pathToMainDrive)
    stats_back = os.statvfs(pathToBackup)
    used_main = (stats_main.f_frsize * (stats_main.f_blocks - stats_main.f_bfree))/1e9
    used_back = (stats_back.f_frsize * (stats_back.f_blocks - stats_back.f_bfree))/1e9
    space_back = (stats_back.f_frsize * stats_back.f_blocks)/1e9
    if abs(used_main - used_back) > maxDiff:
        raise Exception("Drives are different by more than " + str(maxDiff) + "GB. Main drive has " + str(round(used_main,2)) + "GB, backup has " + str(round(used_back,2)) + "GB")
    else:
        successMessage = "main: " + str(round(used_main,2)) + "GB, backup: " + str(round(used_back,2)) + "GB. "

    # check that there is enough space on the destination drive
    if used_main > (space_back):
        raise Exception("Not enough space on destination. Source has " + str(round(used_main,2)) + "GB of data, destination has " + str(round(space_back,2)) + "GB of space")

    # check rsync dry-run
    res = check_output(["rsync","--dry-run","--exclude=lost+found/","--archive","--delete","--stats",pathToMainDrive,pathToBackup])
    res = res.decode("utf-8")
    for line in res.split('\n'):
        if 'Total transferred file size: ' in line:
            nBytes = int(line[line.find(': ')+2:line.rfind(' bytes')].strip().replace(",",""))
    if abs(nBytes/1e9) > maxDiff:
        raise Exception("Dry-run transferring " + str(round(nBytes/1e9,2)) + "GB (more than " + str(maxDiff) + "GB limit)")

    # run actual rsync
    res = check_output(["rsync","--exclude=lost+found/","--archive","--delete","--stats",pathToMainDrive,pathToBackup])
    res = res.decode("utf-8")
    for line in res.split('\n'):
        if 'Total transferred file size: ' in line:
            nBytes = int(line[line.find(': ')+2:line.rfind(' bytes')].strip().replace(",",""))
        if 'Number of created files: ' in line:
            nAddFiles = line[line.find(': ')+2:len(line)].strip().replace(",","")
            if '(' in nAddFiles:
                nAddFiles = nAddFiles[0:nAddFiles.rfind('(')].strip()
        if 'Number of deleted files: ' in line:
            nDelFiles = line[line.find(': ')+2:len(line)].strip().replace(",","")
            if '(' in nDelFiles:
                nDelFiles = nDelFiles[0:nDelFiles.rfind('(')].strip()

    successMessage = successMessage + "rsync added: " + nAddFiles + " files, deleted: " + nDelFiles + " files, transfer: " + str(round(nBytes/1e9,2)) + " GB"

    # --------------------

    # write success
    for line in fileinput.input(logPath,inplace=True):
        print(line.replace("| x | localBackup | HAS NOT RUN |",
            "|" + now.strftime("%-I:%M %p") + "| localBackup | " + successMessage + " |"),end='')
except Exception as e:
    # write error
    for line in fileinput.input(logPath,inplace=True):
        print(line.replace("| x | localBackup | HAS NOT RUN |"
            ,"|" + now.strftime("%-I:%M %p") + "| localBackup | ERROR: " + str(e) + "|"),end='')

"""


# do transfer if it is OK, otherwise abort and send error
print(str(nBytes/1e9) + " GB to be transferred")
if nBytes < maxSize:
    res = call(["rsync","--exclude=lost+found/","--archive","--delete","/mnt/smallssd/","/mnt/bigDrive/"])
    print(res)
else:
    print("Aborting transfer! Transfer amount bigger than " + str(maxSize/1e9) + " GB. (trying to transfer " + str(nBytes/1e9) + " GB)")
"""
