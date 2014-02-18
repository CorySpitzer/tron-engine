#!/usr/bin/python
"""
Logan Davis   Python 2.7.5
Programming workshop

VERY SIMPLE BOT 
a very simple bot that is supposed to be able to run 
a certian length then turn in an order that is simple, but 
also effectively uses space. 

I am currently having problems with the line that defines 'decision'
it is returning a tuple instead of the end of the list

I used the built in logging tool for debugging
found it here: http://docs.python.org/2/howto/logging.html

I found out about the enumerate bit when Sam presented in class
I found more about it here:
http://stackoverflow.com/questions/522563/accessing-the-index-in-python-for-loops

I am trying to work through the list backwards to define decision because
I wish to avoid the possiblity of pulling something out of index range

"""

import random, tron, logging
	
#logging.basicConfig(filename='botlog',level=logging.DEBUG)
#logging.debug('yeah')
#
#logging.debug('---new game---')

def which_move(board):
	"""
	that main body of the 
	botlog
	"""

	dir_list = [4,2,3,1]
	#logging.debug(dir_list)
	for idx,dir in enumerate(dir_list):
		"""
		'should' test if something is passable or not
		"""
		#logging.debug(dir)
		dest = board.rel(dir)
		if not board.passable(dest):
			"""
			pops an item if it isn't passable
			"""
			#logging.debug('not passable')
			trash = dir_list.pop(idx)
			#logging.debug(dir_list)
		
		# decision = dir_list[::-1] #this line is giving me trouble
		decision = dir_list[-1]     # JIM'S FIX
		#logging.debug(decision)
	return decision

for board in tron.Board.generate():
    tron.move(which_move(board))
