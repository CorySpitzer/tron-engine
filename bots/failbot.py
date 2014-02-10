#!/usr/bin/python
"""
 fail.py

 a tron bot which makes an illegal move.
"""
import tron, random

def which_move(board):
    return 'yup'

for board in tron.Board.generate():
    tron.move(which_move(board))
