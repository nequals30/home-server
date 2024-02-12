#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from datetime import datetime
import os

absolutePath = ""

# find the logs directory
curDir = os.path.dirname(os.path.realpath(__file__))
logDir = os.path.join(curDir,'logs')
os.makedirs(logDir, exist_ok=True) # in case it doesn't exist

# write log
now = datetime.now()
logPath = os.path.join(logDir,now.strftime("%Y-%m-%d") + "_log.md")
f = open(logPath,"w")
f.write("### Log for " + now.strftime("%A, %B %d, %Y") + "\n")
f.write("|Time | Task | Message |\n")
f.write("| --- | ---  | ---     |\n")
f.write("|" + now.strftime("%-I:%M %p") + " | startLog | wrote this log |\n")
f.write("| x | localBackup | HAS NOT RUN |\n")
f.close()
