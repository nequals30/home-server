#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from datetime import datetime
import os

# read the config file
config = {}
with open("config.txt","r") as file:
    for line in file:
        k, v = line.strip().split("=",1)
        k = k.strip()
        v = v.strip()
        config[k] = v

# find the logs directory
log_path = config.get("log_path","./logs/") # default to ./logs/
os.makedirs(log_path, exist_ok=True) # make it if it doesnt exist

# write log
now = datetime.now()
log_path = os.path.join(log_path,now.strftime("%Y-%m-%d") + "_log.md")
print(log_path)
f = open(log_path,"w")
f.write("### Log for " + now.strftime("%A, %B %d, %Y") + "\n")
f.write("|Time | Task | Message |\n")
f.write("| --- | ---  | ---     |\n")
f.write("|" + now.strftime("%-I:%M %p") + " | startLog | wrote this log |\n")
f.write("| x | localBackup | HAS NOT RUN |\n")
f.close()
