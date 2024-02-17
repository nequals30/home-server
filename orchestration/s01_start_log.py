#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import runpy

script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '01_logger'))
os.chdir(script_dir)
runpy.run_path('start_log.py')
