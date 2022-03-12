#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from datetime import datetime

absolutePath = ""

now = datetime.now()
f = open(absolutePath + "logs/" + now.strftime("%Y-%m-%d") + "_log.md","w")
f.write("# Log for " + now.strftime("%A, %B %d, %Y") + "\n")
f.write("|Time | Task | Message |\n")
f.write("| --- | ---  | ---     |\n")
f.write("|" + now.strftime("%-I:%M %p") + " | startLog | wrote this log |\n")
f.write("| x | localBackup | HAS NOT RUN |\n")
f.close()
