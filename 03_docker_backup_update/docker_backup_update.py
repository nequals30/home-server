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
    backup_destination = config.get("backup_destination_directory")
    if not os.path.isabs(stacks_directory):
        raise Exception("Stacks directory must be absolute")
    # Todo: check that the backup destination is a path and directory

    # pre-allocate result message variables
    message = ""
    n_good_stacks = 0
    n_good_volumes = 0

    # loop through each stack
    all_stack_paths = [ f.path for f in os.scandir(stacks_directory) \
            if f.is_dir() and f.name!='.git' ]
    for stack in all_stack_paths:
        this_stack_name = os.path.basename(stack)
        backup_file_path = os.path.join(stack, "backup.txt")
        if os.path.exists(backup_file_path):
            try:
                # down stack
                down_stack(stack)

                # read through backup file, and backup selected volumes
                message_backup, this_n_volumes = \
                        backup_stack(stack, backup_destination)
                message = message + message_backup
                n_good_volumes = n_good_volumes + this_n_volumes

                # update stack
                update_stack(stack)

                # up stack
                up_stack(stack)

                n_good_stacks = n_good_stacks + 1

            except Exception as e:
                message = message + "FAILURE on " + this_stack_name + \
                        ": " + str(e) + "\n"
        else:
            message = message + f"WARNING: {os.path.basename(stack)} doesn't have a backup.txt\n"

    # output message
    message = message + f"Ran through {n_good_stacks}.\nBacked up {n_good_volumes} volumes (X GB).\n Pruned X containers (X GB)"
    return message

def down_stack(stack_path):
    subprocess.run("docker compose down", shell=True, cwd=stack_path)

def backup_stack(stack_path, backup_destination):

    # read through backup configuration file
    backup_file_path = os.path.join(stack_path, "backup.txt")
    backup_volumes = []
    with open(backup_file_path,"r") as file:
        for line in file:
            if ":" in line:
                k, v = line.strip().split(":",1)
                if k.lower() == "backup".lower():
                    backup_volumes.append(v.strip())

    # back up each volume with rsync
    message = ""
    n_volumes_good = 0
    for vol in backup_volumes:
        volume_path = os.path.join(stack_path, vol)
        
        # potential errors
        if not os.path.exists(volume_path):
            message = message + "CANT BACKUP, NO SUCH PATH: " + str(volume_path) + "\n"
        elif not (os.listdir(volume_path)):
            message = message + "CANT BACKUP, VOLUME IS EMPTY: " + str(volume_path) + "\n"
        else:

            # call to rsync
            this_stack_name = os.path.basename(stack_path)
            this_destination = os.path.join(backup_destination, this_stack_name)
            command = ['rsync', '--archive', '--delete', \
                    volume_path, this_destination]
            try:
                subprocess.run(command, check=True, stderr=subprocess.PIPE)
                n_volumes_good = n_volumes_good + 1

            except subprocess.CalledProcessError as e:
                message = message + "RSYNC FAILED: " + e.stderr.decode() + "\n"

    return message, n_volumes_good

def update_stack(stack_path):
    subprocess.run("docker compose pull", shell=True, cwd=stack_path)

def up_stack(stack_path):
    subprocess.run("docker compose up -d", shell=True, cwd=stack_path)
    # Note: would be good to have it message whether there were updates

if __name__ == "__main__":
    print(main())
