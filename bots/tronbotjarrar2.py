#!/usr/bin/python
"""
tronbotjarrar2.py

My second bot for a tron tournament. This bot uses the strategy of enemy avoidance. 

Felix Jarrar|Programming Workshop
"""
from tron import *
import random

ORDER = [EAST, WEST, NORTH, SOUTH]

def which_move(board):
    
    candidates = []
    for dir in ORDER:
        dest = board.rel(dir)

        if not board.passable(dest):
            continue

        candidates.append(dir)

        adj = board.adjacent(dest)
    
        if any(board[pos] == THEM for pos in adj):
            continue
        return dir
    
    if candidates:
        return candidates[0]
    
    return EAST

for board in Board.generate():
	move(which_move(board))