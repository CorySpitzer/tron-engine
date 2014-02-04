#!/usr/bin/env python
"""
randlog.py

An example Tron bot which moves in a random direction ... 
and logs what it does to log.txt.

None of these bots can use "print" to show you what it's doing, 
since that's how it communicates with the engine that runs it.
So the simplest way to debug it is to send messages to a log file.

This one can be run with something like this.

 $ ./engines/round.py --replay=games/logexample.tron -B maps/empty-room.txt bots/randbot.py bots/randlog.py 

And it can be then be replayed with html tool via the url

 http://.../replay.html?game_id=logexample
 
"""
import random, tron

class Logger(object):
    def __init__(self, logfilename='logs/log.txt'):
        self.filename = logfilename
        self.file = open(logfilename, 'w')
        self.movenumber = 0
    def out(self, message):
        """ output one line to the log file """
        self.file.write(message + "\n")
    def header(self):
        """ write a header line with incremented move number """
        self.movenumber += 1
        self.out("== move {} ==".format(self.movenumber))
    def footer(self):
        self.out("")

log = Logger()        
    
def which_move(board):
    """ Return a move direction (i.e. 1-4) given a tron Board object. """
    move = random.choice(board.moves())
    log.header()
    log.out(board.as_string())
    log.out("My position is {}".format(board.me()))
    log.out("His position is {}".format(board.them()))
    log.out("My next move is {} which means {}.".format(move, tron.direction(move)))
    log.footer()
    return move

# This part shouldn't need to be changed.
for board in tron.Board.generate():
    tron.move(which_move(board))
