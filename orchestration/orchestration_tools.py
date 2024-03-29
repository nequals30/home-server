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
    try:
        message = this_module.main()
    except Exception as e:
        message = str(e)

    # log the message
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '01_logger')))
    import logger_tools
    logger_tools.log_entry(script_name,message)
