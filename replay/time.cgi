#!/usr/bin/python
"""
 time.cgi

 A tiny example example of a dynamic web program.

 Jim Mahoney | cs.marlboro.edu | Feb 10 2014 | MIT License
"""
import datetime
print "Content-type: text/plain"
print
print "The time is {}.".format(datetime.datetime.now())

