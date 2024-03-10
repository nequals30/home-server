#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import subprocess
import os
import socket

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
            if ',' in v:
                v = [item.strip() for item in v.split(',')]
            config[k] = v

    backup_path = config.get("backup_path")
    exclude_list = config.get("exclude_subdirs")

    # make sure the backup path is an absolute mount point
    if (not os.path.isabs(backup_path)): 
        raise Exception("backup_path must be absolute")
    if not backup_path.endswith("/"):
        raise Exception("backup_path must have a trailing slash")
    if not os.path.ismount(backup_path):
        raise Exception(backup_path + " is not a mountpoint")

    # get current machines hostname
    hn = socket.gethostname()

    # load restic secrets from pass into environment variables
    os.environ['RESTIC_REPOSITORY'] = get_pass_entry(f"{hn}/RESTIC_REPOSITORY")
    os.environ['B2_ACCOUNT_ID'] = get_pass_entry(f"{hn}/B2_ACCOUNT_ID")
    os.environ['B2_ACCOUNT_KEY'] = get_pass_entry(f"{hn}/B2_ACCOUNT_KEY")
    os.environ['RESTIC_PASSWORD'] = get_pass_entry(f"{hn}/RESTIC_PASSWORD")

    temp_cmd = f"restic backup {backup_path} --compression max --exclude-caches --one-file-system --cleanup-cache"
    for subdir in exclude_list:
        temp_cmd += f" --exclude {backup_path}{subdir}"

    print(temp_cmd)

    return "success or fail"

def get_pass_entry(entry_name):
    try:
        return subprocess.run(["pass", entry_name], check=True, capture_output=True, text=True).stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Failed to retrieve {entry_name} from pass: {e}")
        return None


if __name__ == "__main__":
    print(main())
