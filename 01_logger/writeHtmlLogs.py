#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import markdown
import datetime

# read the config file
config = {}
with open("config.txt","r") as file:
    for line in file:
        k, v = line.strip().split("=",1)
        k = k.strip()
        v = v.strip()
        config[k] = v

# interpert the configuration
log_dir = config.get("log_directory","./logs/")
n_days = int(config.get("html_n_days_history","10"))
out_path = config.get("html_out_path","./result.html")

# iterate through the last n days and write logs
now = datetime.datetime.now()
out = ""
for i in range(n_days):
    thisDate = now - datetime.timedelta(days=i)
    this_log_path = os.path.join(log_dir,thisDate.strftime("%Y-%m-%d") + "_log.md")
    try:
        with open(this_log_path, 'r') as md_file:
            md_content = md_file.read()
        out = out + markdown.markdown(md_content, extensions=['tables'])
    except FileNotFoundError:
        out = out + "<h3 style='color: red;'>Missing Log for " + thisDate.strftime("%A, %B %d, %Y") + " !!!</h3>"

# CSS for the page
css = """
<style>
    body {
        background-color: #2f2f2f;
        color: #e8e8e8;
    }
    table {
        border-collapse: collapse;
        width: 70%;
    }
    th, td {
        padding: 15px;
        text-align: left;
    }
</style>
"""

# Write the HTML content to a file
with open(out_path, 'w') as html_file:
    html_file.write(css + out)
