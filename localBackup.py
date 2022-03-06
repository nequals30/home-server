#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from subprocess import check_output,call

# overhead
maxSize = 2e9

# check how many bytes would be transferred
res = check_output(["rsync","--dry-run","--exclude=lost+found/","--archive","--delete","--stats","/mnt/smallssd/","/mnt/bigDrive/"])
res = res.decode("utf-8")
for line in res.split('\n'):
    if 'Total transferred file size: ' in line:
        nBytes = int(line.split(":")[1].replace(" bytes","").strip().replace(",",""))

# do transfer if it is OK, otherwise abort and send error
print(str(nBytes/1e9) + " GB to be transferred")
if nBytes < maxSize:
    res = call(["rsync","--exclude=lost+found/","--archive","--delete","/mnt/smallssd/","/mnt/bigDrive/"])
    print(res)
else:
    print("Aborting transfer! Transfer amount bigger than " + str(maxSize/1e9) + " GB. (trying to transfer " + str(nBytes/1e9) + " GB)")
