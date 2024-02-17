#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from datetime import datetime
import os
import logger_tools

def main():
    # read the config file
    config = logger_tools.read_config()

    # find the logs directory
    log_path = config.get("log_directory")
    os.makedirs(log_path, exist_ok=True)

    # write log
    now = datetime.now()
    log_path = os.path.join(log_path,now.strftime("%Y-%m-%d") + "_log.md")
    f = open(log_path,"w")
    f.write("### Log for " + now.strftime("%A, %B %d, %Y") + "\n")
    f.write("|Time | Task | Message |\n")
    f.write("| --- | ---  | ---     |\n")
    f.write("|" + now.strftime("%-I:%M %p") + " | startLog | wrote this log |\n")
    f.write("| x | localBackup | HAS NOT RUN |\n")
    f.close()
    return "Wrote this log with X scripts"

if __name__ == "__main__":
    print(main())
