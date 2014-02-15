#!/usr/bin/env python
"""
logbot.py

 An example of a random bot which writes debug messages
 and errors to a log file.

 See the details of this approach to debugging in tron.py .

 Jim M | cs.marlboro.edu | Feb 2014 

"""
import random, tron

DEBUG = True

if DEBUG:
    #      On csmarlboro.org, change 'everyone' to your username.
    #      Keep the rest of the path - that folder is world writable.
    #      This opens that file for appending, and writes one line
    #      to it with the date and time.
    logfile = '/var/www/csmarlboro/tron/logs/everyone.txt'
    tron.init_error_log(logfile)
    tron.warn("Starting logbot")   # Change this to whatever you like.

def debug(message):
    if DEBUG:
        tron.warn(message)

def which_move(board):
    """ Return the direction to move (1,2,3,4) given a Board object. """
    choices = board.moves()
    debug('')
    debug(' legal moves are' + str(choices))
    move = random.choice(choices)
    debug(' chosen move is ' + str(move))
    
    if random.randint(1,10) == 3: a = 1/0    # sometimes do something bad.
                                             # (This error will be in the log.)
    return move

# Your probably don't need to change this part.
for board in tron.Board.generate():
    tron.move(which_move(board))
