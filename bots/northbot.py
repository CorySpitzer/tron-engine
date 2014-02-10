#!/usr/bin/python
"""
 northbot.py

 a trivial tron robot
"""
import tron, random

def which_move(board):
    return tron.NORTH

for board in tron.Board.generate():
    tron.move(which_move(board))
