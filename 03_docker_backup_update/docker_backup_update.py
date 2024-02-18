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

    # down the stacks
    all_stack_paths = [ f.path for f in os.scandir(stacks_directory) if f.is_dir() ]
    for stack in all_stack_dirs:
        result = subprocess.run("pwd", shell=True, cwd=stack, capture_output=True, text=True)
        print(result)

    return "success message"

if __name__ == "__main__":
    print(main())
