#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from datetime import datetime

absolutePath = ""

now = datetime.now()
f = open(absolutePath + "logs/" + now.strftime("%Y-%m-%d") + "_log.html","w") 
f.write("<html><body>")
f.write("Log started on " + now.strftime("%A, %B %d at %-I:%M %p"))
f.write("</body</html>")
f.close()
