#!/usr/bin/env python
"""
simplelogbot.py

A simple example of writing to a log file.

"""
import random, tron

DEBUG = True
if DEBUG:
    logfile = open('simplelog.txt', 'a')
def debug(message):
    if DEBUG:           # Write to logfile ?
        logfile.write(message)

debug('---- starting game ----\n')

def which_move(board):
    """ Return the direction to move (1,2,3,4) given a Board object. """
    choices = board.moves()
    debug(' * \n')
    debug(' legal moves are' + str(choices) + '\n')
    move = random.choice(choices)
    debug(' next move is ' + str(move) + '\n')
    return move

# Your probably don't need to change this part.
for board in tron.Board.generate():
    tron.move(which_move(board))
