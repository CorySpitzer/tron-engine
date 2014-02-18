#!/usr/bin/python
 """
 DOESN'T WORK!!!
 I have messed around with the code a great deal
 I think I just need more time with it
 the idea is that it will locate where it is on the board 
 then travel on it's y axis until it meets with the other player on it's x axis
 after that meeting occurs, in it's current state it should just wall hug.
 once I get this to work, i will add another section that cuts across the board directly,
 effectively cuting down the oppenents portion of the board by a great portion.
 Buuuuuut it doesn't work right now.
"""

 import tron, random
 
 ORDER = list(tron.DIRECTIONS)
 random.shuffle(ORDER)
 
 def which_move(board):
    
    #figures out where the other player is starting and where you are starting

    y_relation = ''
    x_relation = ''
    me = tron.me()
    them = tron.them()

    if them[0] > me[0]:
        y_relation = 'down'
    else:
        y_relation = 'up'
    if them [1] > me[1]:
        x_relation = 'right'
    else:
        x_relation = 'left'
    


    if y_relation == 'down':
        distance_y = them[0]
    else:
        distance_y = me[0]
    if x_relation == 'right'
        distance_x = them[1]
    else: 
        distance_x = me[0]
    
    #The bot starts moving with this section, currently it only travels up half the board.   
    if count == 0:


        if y_relation == 'down':

        
            dest = board.rel(SOUTH)

            if not board.passable(dest):
                dest = board.rel(EAST)
            else:
                pass

            decision = dest
            return decision
        if distance_y == 'up':
            dest = board.rel(NORTH)

            if not board.passable(dest):
                dest = board.rel(WEST)
            else:
                pass
            decision = dest
            return decision
 
        
    #later a middle phase will be added so the bot will cut the board in 2
 
    #once the two players cross on the x-axis, this should be what moves the bot
    if count == 1:
 
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
 
        return decision
 
 #  make a move each turn
 count = 0
 for board in tron.Board.generate():
    
    tron.move(which_move(board))
    if count == 0:
        if tron.me[1] ==tron.them[1]:
                count = 1
    else: 
        #placed for clarity
        pass