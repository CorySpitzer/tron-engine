#!/usr/bin/python
"""
tronbotjarrar.py

A start at a tronbot.
http://tron.aichallenge.org

#notes from class
chmod +x botname.py

Some stuff I'll want to implement:

./logbot.py < input.txt

more log.txt

more command types the files out

def denug(message):
	if True:
		if logfile == None:
			logfile.write(message)
logfile = open('logfile.txt', 'a')

logfile.write('--Starting

Felix Jarrar|Programming Workshop
"""

from tron import *
import random

ORDER = [EAST, SOUTH, NORTH, WEST]

def which_move(board):
	for dir in ORDER:
		dest = board.rel(dir)
    
		if board.passable(dest):
			return dir

	return EAST
	
for board in Board.generate():
	move(which_move(board)) 

#(y,x) = board.me()

#if board[0,4] == tron.FLOOR:
#	do_something()
    
#for board in Board.generate():
#	move(which_move(board)) 