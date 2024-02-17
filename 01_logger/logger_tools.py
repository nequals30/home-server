#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os

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
