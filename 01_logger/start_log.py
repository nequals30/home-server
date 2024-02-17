#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from datetime import datetime
import os
import logger_tools

def main():
    # read the config file
    config = logger_tools.read_config()
    log_path = config.get("log_directory")

    # make the logs folder if it doesnt exist
    os.makedirs(log_path, exist_ok=True)

    # write log
    now = datetime.now()
    log_path = os.path.join(log_path,now.strftime("%Y-%m-%d") + "_log.md")
    f = open(log_path,"w")
    f.write("### Log for " + now.strftime("%A, %B %d, %Y") + "\n")
    f.write("|Time | Task | Message |\n")
    f.write("| --- | ---  | ---     |\n")
    f.write("| X | start_log | HAS NOT RUN |\n")
    f.write("| X | localBackup | HAS NOT RUN |\n")
    f.write("| X | end_write_logs | HAS NOT RUN |\n")
    f.close()
    return "Wrote this log with X scripts"

if __name__ == "__main__":
    print(main())
