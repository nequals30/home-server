#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from datetime import datetime
import os

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

    # find the logs directory
    log_path_default = os.path.join(this_dir,'./logs/') # default to ./logs/
    log_path = config.get("log_directory",log_path_default)
    if (log_path[:2] == "./") or (log_path[:3] == "../"):
        log_path = this_dir + "/" + log_path
    os.makedirs(log_path, exist_ok=True) # make it if it doesnt exist

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
