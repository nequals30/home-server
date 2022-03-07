#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from datetime import date

f = open("logs/" + str(date.today()) + "_log.html","w") # make this a relative path in config file
f.write("<html><body>test of logging functionality</body</html>")
f.close()
