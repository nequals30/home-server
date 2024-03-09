#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import subprocess
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

    backup_path = config.get("backup_path")

    # make sure the backup path is an absolute mount point
    if (not os.path.isabs(backup_path)): 
        raise Exception("backup_path must be absolute")
    if not backup_path.endswith("/"):
        raise Exception("backup_path must have a trailing slash")
    if not os.path.ismount(backup_path):
        raise Exception(backup_path + " is not a mountpoint")

    return "success or fail"


def get_pass_entry(entry_name):
    try:
        return subprocess.run(["pass", entry_name], check=True, capture_output=True, text=True).stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Failed to retrieve {entry_name} from pass: {e}")
        return None


if __name__ == "__main__":
    print(main())
