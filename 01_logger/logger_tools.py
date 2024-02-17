#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
from datetime import datetime
import fileinput 

def read_config():
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

    # convert any filepaths to be absolute based on this directory
    path_fields = ['log_directory','html_out_path']
    for field in path_fields:
        this_path = config[field]
        if not os.path.isabs(this_path):
            config[field] = os.path.join(this_dir, this_path)

    return config


def log_entry(script_name, message):
    # read the config file
    config = read_config()
    log_path = config.get("log_directory")

    # open the MD file
    now = datetime.now()
    log_path = os.path.join(log_path,now.strftime("%Y-%m-%d") + "_log.md")

    # find the right row to replace
    for line in fileinput.input(log_path, inplace=True):
        print(line.replace("| X | " + script_name + " | HAS NOT RUN |",
            "|" + now.strftime("%-I:%M %p") + "| " + script_name + " | " + message + " |"),end='')
