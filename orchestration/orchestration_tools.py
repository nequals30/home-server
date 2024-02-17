#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import sys
from importlib import import_module

def run_script(script_folder, script_name):
    # switch to script_folder and run script_name in the folder
    script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', script_folder))
    sys.path.append(script_dir)
    this_module = import_module(script_name)
    message = this_module.main()
    print(message)
