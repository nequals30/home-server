#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import markdown
import datetime
import logger_tools

def main():
    # read the config file
    config = logger_tools.read_config()
    log_dir = config.get("log_directory")
    out_path = config.get("html_out_path")
    n_days = int(config.get("html_n_days_history","10"))

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

    return "Created this HTML file"

if __name__ == "__main__":
    print(main())
