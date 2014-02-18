#!/usr/bin/python
"""
The purpose of this tron bot is simply to run with a minimal amount of
intelligence behind each move.

The algorithm is based on the wallbot but rather than looking to move
along the wall, it looks to move - if possible - to a location with
one open adjacent move.

Following bot based on wallbot from the tron.aichallenge website.

(The original was intended to look farther ahead but I got caught up
in the details - basically I was trying
"""

import tron, random

ORDER = list(tron.DIRECTIONS)
random.shuffle(ORDER)

def which_move(board):

    for i in ORDER:
        
        decision = board.moves()[0]
                        
        #looking at area directly surrounding 
        landing = board.rel(i)
                                
        #finding legal moves within surrounding area
        if not board.passable(landing):
            continue
                                        
        #defining the squares adjacent to chosen legal move (looking 2 steps ahead)
        adj = board.adjacent(landing)
                                                
        if any(board[place] == tron.FLOOR for place in adj):
            decision = i 
            break
                                                                        
        #for place in adj:
                #defining the squares 3 steps ahead
                #adj2 = board.adjacent(place)
                #if 2 and 3 steps ahead are open, move to the place that allows for that 
                #if any (board[place] == tron.FLOOR and 
                        # ( board[p2] == tron.FLOOR for p2 in adj2 )):
                                                              
    return decision


for board in tron.Board.generate():
    tron.move(which_move(board))
