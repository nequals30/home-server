#!/usr/bin/env python3
#-*- coding: utf-8 -*-

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

    # get the stacks directory
    stacks_directory = config.get("stacks_directory")
    if not os.path.isabs(stacks_directory):
        raise Exception("Stacks directory must be absolute")

    # loop through each stack
    message = ""
    n_good = 0
    all_stack_paths = [ f.path for f in os.scandir(stacks_directory) \
            if f.is_dir() and f.name!='.git' ]
    for stack in all_stack_paths:
        backup_file_path = os.path.join(stack, "backup.txt")
        if os.path.exists(backup_file_path):
            print(f"{os.path.basename(stack)}: yes")
            n_good = n_good + 1
        else:
            print(f"{os.path.basename(stack)}: no")
            message = message + f"WARNING: {os.path.basename(stack)} doesn't have a backup.txt\n"

    # output message
    message = f"successfully backed up {n_good} stacks\n" + message
    return message

if __name__ == "__main__":
    print(main())
