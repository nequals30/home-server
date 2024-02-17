#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
from subprocess import check_output,call

def main():
    # read the config file
    this_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(this_dir,'config.txt')
    config = {}
    with open(config_path,"r") as file:
        for line in file:
            k, v = line.strip().split("=",1)
            k = k.strip()
            v = v.strip()
            config[k] = v

    pathToMainDrive = config.get("main_directory")
    pathToBackup = config.get("backup_directory")
    maxDiff = int(config.get("max_diff_gb"))

    # make sure the file paths are absolute
    if (not os.path.isabs(pathToMainDrive)) or (not os.path.isabs(pathToBackup)):
        raise Exception("drive paths must be absolute")

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

    return successMessage

if __name__ == "__main__":
    print(main())
