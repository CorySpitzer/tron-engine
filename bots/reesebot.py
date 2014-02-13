#!/usr/bin/python
"""
John Reese
Feb  13, 2014
Tron AI challenge
"""
import tron
import random
from sys import exit

logfile = open('logfile.txt','w+')
logfile.write('-------NEW GAME--------\n')
def log(message):
	"""
	logs the message string to the logfile in line 12.
	"""
	logfile.write(message + '\n')
	logfile.flush()

class MoveError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class Game(object):
	def __init__(self, board):
		self.board = board
		self.me_x,self.me_y = board.me()
		self.them_x,self.them_y = board.them()
		log('created game object')


	def try_move(self,direction):
		log('trying move ' + str(direction) + '...')
		if direction in self.board.moves():
			log('move is valid. Sending move: ' + str(direction))
			print direction
			exit()
		else:
			log('move not valid, raising MoveError: ' + str(direction))
			raise MoveError('Move not valid: ' + str(direction))

	def get_closer_start(self):
		"""This function gets ME closer to the other bot
		It calls get_closer_vert/horiz to actually make the move
		all moves are done through try,except so that no invalid moves shold be made."""
		log('starting get_closer_start')
		y_diff = self.them_y - self.me_y
		x_diff = self.them_x - self.me_x
		if abs(y_diff)>abs(x_diff):
			try:
				log('trying get_closer_vert')
				self.try_move(self.get_closer_vert(y_diff))
			except MoveError:
				self.fallback()
		elif abs(y_diff)<abs(x_diff):
			log('trying get_closer_horiz')
			try:
				self.try_move(self.get_closer_horiz(y_diff))
			except MoveError:
				self.fallback()
		elif abs(y_diff) == abs(x_diff):
			log('trying to pick get_closer_vert or get_closer_horiz')
			try:
				self.try_move(random.choice([self.get_closer_vert(y_diff), self.get_closer_horiz(x_diff)]))
			except MoveError:
				self.fallback()
				
	def get_closer_vert(self,y_diff):
		log('in get_closer_vert')
		if y_diff>0:
			log('y_diff>0, returning tron.SOUTH')
			return tron.SOUTH
		if y_diff<0:
			log('y_diff<0, returning tron.NORTH')
			return tron.NORTH

	def get_closer_horiz(self,x_diff):
		if x_diff>0:
			log('x_diff>0, returning tron.EAST')
			return tron.EAST
		if x_diff<0:
			log('x_diff<0, returning tron.WEST')			
			return tron.WEST

	def fallback(self):
		log('trying fallback!')
		bestcount = -1
		bestmove = tron.NORTH
		for dir in self.board.moves():
			dest = self.board.rel(dir)
			count = 0
			for pos in self.board.adjacent(dest):
				if self.board[pos] == tron.FLOOR:
					count += 1
			if count > bestcount:
				bestcount = count
				bestmove = dir
		print bestmove
		exit()

def which_move(board):
	log('in which_move()')
	game = Game(board)
	game.get_closer_start()
	fallback()

for board in tron.Board.generate():
	tron.move(which_move(board))