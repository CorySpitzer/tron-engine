#!/usr/bin/env python

"""
kamikazebot.py

Runs at the enemy bot.

Everest Witman	 2014	Programming Workshop
"""

import math, tron

def distance(one, two):
	# Finds the distance between two points
	
	y1, x1 = one 
	y2, x2 = two

	distance = math.sqrt((y2 - y1)**2+(x2 - x1)**2)
	return distance

def which_move(board):
	# Chooses which move to make each turn

	moves = list(board.moves())
	decision = tron.NORTH
    
	for dir in moves:
		if distance(board.rel(dir), board.them()) <= distance (board.rel(decision), board.them()):
			decision = dir

	return decision

# make a move each turn
for board in tron.Board.generate():
    tron.move(which_move(board))

