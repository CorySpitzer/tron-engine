#!/usr/bin/env python
"""
randbot.py

An example Tron bot which moves in a random direction.

There's a lot of tricky stuff going on behind the scenes
here which you can probably mostly ignore. On each turn,
this program will read an entire board position from stdin
(which is supplied by the engine that runs it), and then
needs to print to stdout the direction it wants to move
as an integer from 1 to 4.

To write your own bot, modify which_board() to return
the best move given the board, which is a Board object
as described in tron.py

See randlog.py for a similar bot with debugging output.

"""
import random, tron

def which_move(board):
    """ Return the direction to move (1,2,3,4) given a Board object. """
    return random.choice(board.moves())

# Your probably don't need to change this part.
for board in tron.Board.generate():
    tron.move(which_move(board))
