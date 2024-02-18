#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import subprocess

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
        this_stack_name = os.path.basename(stack)
        backup_file_path = os.path.join(stack, "backup.txt")
        if os.path.exists(backup_file_path):
            try:
                # down stack
                down_stack(stack)
                print("stack down: " + this_stack_name)

                # read through backup file, and backup selected volumes
                backup_stack(stack)

                # update stack
                update_stack(stack)
                print("update stack: " + this_stack_name)

                # up stack
                up_stack(stack)
                print("stack back up: " + this_stack_name)

                n_good = n_good + 1

            except Exception as e:
                message = message + "FAILURE on " + this_stack_name + \
                        ": " + str(e) + "\n"
        else:
            message = message + f"WARNING: {os.path.basename(stack)} doesn't have a backup.txt\n"

    # output message
    message = f"successfully backed up {n_good} stacks\n" + message
    return message

def down_stack(stack_path):
    subprocess.run("docker compose down", shell=True, cwd=stack_path)

def backup_stack(stack_path):
    # read through backup file
    message = ""
    backup_file_path = os.path.join(stack_path, "backup.txt")
    backup_volumes = []
    with open(backup_file_path,"r") as file:
        for line in file:
            if ":" in line:
                k, v = line.strip().split(":",1)
                if k.lower() == "backup".lower():
                    backup_volumes.append(v.strip())

    # back up each volume with rsync
    for vol in backup_volumes:
       volume_path = os.path.join(stack_path, vol)
       if not os.path.exists(volume_path):
           message = message + "NO SUCH PATH: " + str(volume_path)
       else:
           print("backing up " + str(volume_path)
    print("message")

def update_stack(stack_path):
    subprocess.run("docker compose pull", shell=True, cwd=stack_path)

def up_stack(stack_path):
    subprocess.run("docker compose up -d", shell=True, cwd=stack_path)

if __name__ == "__main__":
    print(main())
