#!/usr/bin/python
"""
 tourney.cgi

 Generate a web page with clickable links to the games in a tournament.

 http://..../tourney.cgi?name=<name>   where <name> is e.g. test

 Jim Mahoney | cs.marlboro.edu | Feb 2014 | MIT License
"""
import cgitb         # online debugging
cgitb.enable()

import cgi, os
print "Content-type: text/html"
print

params = cgi.FieldStorage()
name = params['name'].value
games = os.listdir('../games/' + name)
links = '\n'.join(
    map(lambda x: '<a href="{}">{}</a><br>'.format('index.html?game_id='+x, x),
        map(lambda x: '{}/{}'.format(name, x[:-5]), 
            games)))
html = open('tourney_template.html').read()
result = ''.join(
    open('../tournaments/{}/result.txt'.format(name)).readlines()[-6:])

print html.format(name=name, links=links, result=result)


