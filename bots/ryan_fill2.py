#!/usr/bin/env python
'''
	Tron bot that chooses moves into the largest possible free area.
	Ryan Merrill using library and stub by Jim Mahoney.
'''
import random, tron


########## Find free area around square ##############
def area_finder(board,square_coordinates):
	if not board.passable(square_coordinates):
		return 0
	UNSEEN='u'
	SEEN='s'
	area=0
	
	#Create map to keep track of which areas have been seen by algorithm
	map=[]
	for line in xrange(board.height):
		map.append([])
	for line in map:
		for i in xrange(board.width):
			line.append(UNSEEN)
	
	#Expand out into adjacent unseen squares
	fringe=[square_coordinates]
	map[square_coordinates[0]][square_coordinates[1]]=SEEN
	while len(fringe) > 0:
		area+=1
		for sq in board.adjacent(fringe[0]):
			if board.passable(sq):
				if map[sq[0]][sq[1]]==UNSEEN:
					fringe.append(sq)
					map[sq[0]][sq[1]]=SEEN
		del fringe[0]
	return area

	


def which_move(board):

	#unused test info dump to file
    '''
    f=open("tronoutput.txt", 'w')
    s=''
    for line in board.board:
    	s=s+str(line)+'\n'
    f.write(s)
    f.close
    '''
    moves=(1,2,3,4)
    # Make move into largest free area or default to north.
    best_move=1
    best_area = 0
    for move in moves:
    	sq=board.rel(move)
    	area = area_finder(board,sq)
    	if area > best_area:
    		best_area = area
    		best_move = move
    return best_move

# Get board and make move
for board in tron.Board.generate():
    tron.move(which_move(board))
