#!/usr/bin/python
"""
John Reese
Feb  10, 2014
Tronbot
"""
import tron
import random

ORDER = list(tron.DIRECTIONS)
random.shuffle(ORDER)
logfile = open('logfile.txt','r+')
def log(message,logfile):
	logfile.write(message + '\n')
	logfile.flush()


def distance_apart(board): 
	"""NOT USED
	returns the number of blocks it would take to reach
	the other player, provided he is stationary."""
	return abs(board.me()[0]+board.them()[0]) + abs(board.me()[1] + board.them()[1])
x = True
y = False
def which_move(board):
	log('passible moves: ' + str(board.moves()),logfile)
	them_y,them_x = board.them()
	me_y,me_x = board.me()
	log('my position = ' + str((me_y, me_x)),logfile)
	log('their position = ' + str((them_y, them_x)),logfile)
	y_diff = them_y - me_y
	x_diff = them_x - me_x
	log('x_diff = ' + str(x_diff),logfile)
	log('y_diff = ' + str(y_diff),logfile)
	if abs(y_diff)>abs(x_diff):
		log('elif y_diff > x_diff',logfile)		
		log('Is the NORTH valid and towards the opponent ?' + str(y_diff<0 and board.passable(board.rel(tron.NORTH))),logfile)
		log('Is the SOUTH valid and towards the opponent ?' + str(y_diff>0 and board.passable(board.rel(tron.SOUTH))),logfile)
		if y_diff<0 and board.passable(board.rel(tron.NORTH)):
			log('y_diff<0, going NORTH',logfile)
			# log('returning tron.NORTH',logfile)
			return tron.NORTH
		elif y_diff>0 and board.passable(board.rel(tron.SOUTH)):
			log('y_diff>0, going SOUTH',logfile)
			# log('returning tron.SOUTH',logfile)
			return tron.SOUTH
		# elif not board.passable(board.rel(tron.NORTH)) and not board.passable(board.rel(tron.SOUTH)):
		else:
			# randbot(board)
			i = 0
			while x==True:
				log('entering first weird while loop', logfile)
				if board.passable((me_y,me_x+i))==True:
					i = i + 1
				else:
					x=False
			log('there are ' + i +' squares WEST',logfile)
			j = 0
			while y==True:
				if board.passable((me_y,me_x-j))==True:
					j = j + 1
				else:
					y=False
			log('there are ' + j +' squares EAST',logfile)
			if i>=j:
				return tron.EAST
			else:
				return tron.WEST

	elif abs(y_diff)<abs(x_diff):
		log('elif y_diff < x_diff',logfile)
		log('Is the EAST valid and towards the opponent? ' + str(y_diff>0 and board.passable(board.rel(tron.EAST))),logfile)
		log('Is the WEST valid and towards the opponent? ' + str(y_diff<0 and board.passable(board.rel(tron.WEST))),logfile)
		if x_diff>0 and board.passable(board.rel(tron.EAST)):
			log('x_diff>0, going EAST',logfile)
			return tron.EAST
		elif x_diff<0 and board.passable(board.rel(tron.WEST)):
			log('x_diff<0, going WEST',logfile)
			return tron.WEST
		# elif not board.passable(board.rel(tron.EAST)) and not board.passable(board.rel(tron.WEST)):
		else:

			i = 0
			while x == True:
				log('entering second weird while loop', logfile)

				if board.passable((me_y+i,me_x))==True:
					i = i + 1
				else:
					x = False
			log('there are ' + i +' squares NORTH',logfile)
			j = 0
			while y == True:
				if board.passable((me_y-j,me_x))==True:
					j = j + 1
				else:
					y = False
			log('there are ' + i +' squares SOUTH',logfile)
			if i>=j:
				log('moving NORTH'.logfile)
				return tron.NORTH
			else:
				log('moving SOUTH',logfile)
				tron.SOUTH
	elif y_diff == x_diff:
		return wallbot(board)
		# return randbot(board)
		# return random.choice(board.moves())
def randbot(board):
	log('randomtime', logfile)
	choices = board.moves()
	log(str(choices),logfile)
	return choices[0]

def wallbot(board):

    decision = board.moves()[0]

    for dir in ORDER:

        # where we will end up if we move this way
        dest = board.rel(dir)

        # destination is passable?
        if not board.passable(dest):
            continue

        # positions adjacent to the destination
        adj = board.adjacent(dest)

        # if any wall adjacent to the destination
        if any(board[pos] == tron.WALL for pos in adj):
            decision = dir
            break
    log(str(decision),logfile)
    return decision

def flood_fill(board, ypos, xpos): 
	"""NOT DONE"""
	boardlist = board.board.split('\n')
	for row in range(len(boardlist)):
		boardlist[row] = list(boardlist[row])
	boardlist[ypos][xpos] = '0'
	# for direction in board.moves():
	if board.passable(board.adjacent((ypos,xpos))[0]) == tron.FLOOR: # up
		flood_fill(board, ypos+1, xpos)

	if board.passable(board.adjacent((ypos,xpos))[1]) == tron.FLOOR: # right
		flood_fill(board, ypos, xpos+1)

	if board.passable(board.adjacent((ypos,xpos))[2]) ==tron.FLOOR: # down
		flood_fill(board, ypos-1, xpos)

	if board.passable(board.adjacent((ypos,xpos))[3]) == tron.FLOOR: # left
		flood_fill(board, ypos, xpos-1)


for board in tron.Board.generate():
	tron.move(which_move(board))
