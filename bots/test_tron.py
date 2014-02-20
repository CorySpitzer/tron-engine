"""
test_tron.py

A playground for testing the tron.py library and some algorithms.

Usage:

    $ python test_tron.py - v          # -v is 'verbose' : see tests
    
  or
 
    $ python
    >> from test_tron import *
    >> watch_flood()                   # output at bottom of file
    ...
    >> ... try interactively things like those below
    
Tests:

    >>> board = new_board(EMPTY_ROOM)

    >>> board.me()                          # My location (row, column))
    (1, 1)
    >>> board.them()                        # Opponent's location
    (13, 13)
    >>> board.rel(EAST)                     # Location to my east
    (1, 2)
    >>> board.rel(EAST, (1,2))              # Location east of that
    (1, 3)
    >>> board.adjacent( (1,3) )             # Neigbors of (1, 3)
    [(0, 3), (1, 4), (2, 3), (1, 2)]

    # Which of the cells next to (1,3)  are floor tiles ?
    >>> filter(lambda cell: board[cell]==FLOOR, board.adjacent((1,3)))
    [(1, 4), (2, 3), (1, 2)]

    >>> board.moves()                       # Which directions can I move?
    [2, 3]
    >>> map(tron.direction, board.moves())  # Same, but translated to names
    ['east', 'south']

    # Is the location to the east of me a floor?
    # (This is the API from tron.py - awkward. We could do better.)
    >>> board[board.rel(EAST, board.me())] == FLOOR
    True

    >> same_room(new_board(EMPTY_ROOM), ME, THEM)   # Can the players collide?
    True
    >> same_room(new_board(SPLIT_ROOM), ME, THEM)   # Same, different room.
    False

    >> reachable_space(new_board(SPLIT_ROOM), ME)   # Size of area I'm in?
    9 
    >> reachable_space(new_board(SPLIT_ROOM), THEM) # Size of area they're in?
    19
    
For more information see ./tron.py for the basic notions and conventions,
and https://github.com/MarlboroCollegeComputerScience/tron-engine for
the Tron AI protocols and infrastructure.

Tested with Python 2.7.5
    
Jim Mahoney, Marlboro College | MIT License | Feb 2014
"""
from tron import Board,  NORTH, SOUTH, EAST, WEST,  FLOOR, WALL, ME, THEM
import tron   # tron.move, tron.warn, tron.init_error_log, tron.direction

EMPTY_ROOM = [ "###############",   # ../maps/empty-room.txt
               "#1            #",
               "#             #",
               "#             #",
               "#             #",
               "#             #",
               "#             #",
               "#             #",
               "#             #",
               "#             #",
               "#             #",
               "#             #",
               "#             #",
               "#            2#",
               "###############"  ]

SPLIT_ROOM = [ "#########",
               "#1  #   #",
               "#   #   #",
               "#   #   #",
               "#####   #",
               "#      2#",
               "#########"  ]

def new_board(grid=EMPTY_ROOM):
    """ Return a board [default empty room] """
    return Board(len(grid[0]), len(grid), grid)

def _place(board, where):
    """ A location, allowing ME and THEM as shorthands
        >>> _place(new_board(EMPTY_ROOM), ME)
        (1, 1)
        >>> _place(new_board(EMPTY_ROOM), THEM)
        (13, 13)
        >>> _place(new_board(EMPTY_ROOM), (5, 4))
        (5, 4)
    """
    if where == ME:
        return board.me()
    elif where == THEM:
        return board.them()
    else:
        return where

def flood(board, function, origin=ME, verbose=False):
    """ Do function(board, location) on all non-wall places
        reachable from origin """
    # Notes :
    #  * The algorithm is given at http://en.wikipedia.org/wiki/Flood_fill .
    #    This is the recursive version.
    #  * Here we uses the python "set" data structures to avoid repitition.
    #  * Essentially this a loop over all reachable locations.
    #  * Depending on 'function', it can calculate a number of things.
    #  * Graph search algorithms like this use the word "fringe" 
    #    for the places that have been found but not examined yet.
    #
    if verbose: print "-- flood -- function={}".format(function.func_name)
    if verbose: print board.as_string()
    fringe = set([_place(board, origin)])  # places left to look at
    visited = set()                        # places already looked at (none)
    while len(fringe) > 0:                 # Anything left to do?
        if verbose: print " * fringe len={} : {}".format(len(fringe), fringe)
        if verbose: print "   visited len={} : {}".format(len(visited), visited)
        location = fringe.pop()                  # Pick one to look at.
        visited.add(location)                    # Add to what we've seen.
        if verbose: print "   looking at location = {}".format(location)
        if board[location] != WALL:              # Is it a non-floor tile?
            if verbose: print "   call function"
            function(board, location)                # Apply function to it.
            fringe |= set(board.adjacent(location))  # Add neighbors to fringe.
            fringe -= visited                        # Remove ones we've done.

def reachable_space(board, origin=ME):
    """ Return the number of spots a bot can get to from the origin """
    # There's some tricky python stuff going on here.
    # We define a function within a function, which lets inc_counter
    # access the 'count' variable which is in its scope.
    # (You almost never want to do this in python.)
    # However, *assigning* 'count' to something within inc_counter
    # (for example trying 'count += 1') throws an error, in the same
    # way that modifying a global variable from a function throws an error.
    # The trick I'm doing here lets inc_counter modify a property of
    # count, without modifying count itself, i.e. while keeping id(count)
    # the same. Somewhat awkward, but hey - it seems to work.
    count = {'spaces' : 0}   # A kludge to keep id(count) remain fixed.
    def inc_counter(board, location):
        count['spaces'] += 1
    flood(board, inc_counter, origin)
    return count['spaces']

def same_room(board, where1=ME, where2=THEM):
    """ Can where1 move to where2? (default ME, THEM) """
    location2 = _place(board, where2)
    reachable = {'location2' : False}   # same kludge as in reachable_space
    def find_location2(board, location):
        if location == location2:
            reachable['location2'] = True
    flood(board, find_location2, where1)
    return reachable['location2']

def matrix_to_string(grid):
    """ Return a string form of rectangular matrix,
        for example [['a', 'b'], ['c', 'd']] becomes "ab\ncd" """
    result = ""
    for row in grid:
        for char in row:
            result += char
        result += "\n"
    return result

def watch_flood(board=new_board(SPLIT_ROOM), origin=ME):
    """ print successive steps of the flood search """
    matrix = [[None]*board.width for i in range(board.height)]
    for y in range(board.height):
        for x in range(board.width):
            matrix[y][x] = board[y,x]
    ## debugging
    # print "-- board -- "
    # print board.as_string()
    # print "-- matrix -- "
    # print matrix_to_string(matrix)
    def mark_and_print(board, location):
        y, x = location
        matrix[y][x] = "x"
        print matrix_to_string(matrix)
    flood(board, mark_and_print, ME, True)

if __name__ == '__main__':
    # The Python doctest testing framework :
    # see http://docs.python.org/2/library/doctest.html
    import doctest
    doctest.testmod()
    
    ## print an analysis of the flood() algorithm
    # watch_flood()


"""
# Output from watch_flood()

    
$ python
Python 2.7.5 (default, May 19 2013, 13:26:46) 
[GCC 4.2.1 Compatible Apple Clang 4.1 ((tags/Apple/clang-421.11.66))] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from test_tron import *
>>> watch_flood()
-- flood -- function=mark_and_print
#########
#1  #   #
#   #   #
#   #   #
#####   #
#      2#
#########

 * fringe len=1 : set([(1, 1)])
   visited len=0 : set([])
   looking at location = (1, 1)
   call function
#########
#x  #   #
#   #   #
#   #   #
#####   #
#      2#
#########

 * fringe len=4 : set([(0, 1), (1, 2), (1, 0), (2, 1)])
   visited len=1 : set([(1, 1)])
   looking at location = (0, 1)
 * fringe len=3 : set([(1, 2), (1, 0), (2, 1)])
   visited len=2 : set([(0, 1), (1, 1)])
   looking at location = (1, 2)
   call function
#########
#xx #   #
#   #   #
#   #   #
#####   #
#      2#
#########

 * fringe len=5 : set([(1, 3), (2, 2), (1, 0), (2, 1), (0, 2)])
   visited len=3 : set([(0, 1), (1, 2), (1, 1)])
   looking at location = (1, 3)
   call function
#########
#xxx#   #
#   #   #
#   #   #
#####   #
#      2#
#########

 * fringe len=7 : set([(2, 3), (1, 4), (2, 2), (1, 0), (0, 3), (2, 1), (0, 2)])
   visited len=4 : set([(0, 1), (1, 2), (1, 3), (1, 1)])
   looking at location = (2, 3)
   call function
#########
#xxx#   #
#  x#   #
#   #   #
#####   #
#      2#
#########

 * fringe len=8 : set([(3, 3), (1, 4), (0, 2), (2, 1), (2, 2), (2, 4), (1, 0), (0, 3)])
   visited len=5 : set([(0, 1), (1, 2), (1, 3), (2, 3), (1, 1)])
   looking at location = (3, 3)
   call function
#########
#xxx#   #
#  x#   #
#  x#   #
#####   #
#      2#
#########

 * fringe len=10 : set([(3, 2), (1, 4), (0, 2), (2, 1), (4, 3), (2, 2), (2, 4), (1, 0), (3, 4), (0, 3)])
   visited len=6 : set([(0, 1), (1, 2), (1, 3), (3, 3), (2, 3), (1, 1)])
   looking at location = (1, 4)
 * fringe len=9 : set([(3, 2), (0, 2), (2, 1), (4, 3), (2, 2), (2, 4), (1, 0), (3, 4), (0, 3)])
   visited len=7 : set([(0, 1), (1, 2), (1, 3), (3, 3), (1, 4), (2, 3), (1, 1)])
   looking at location = (0, 2)
 * fringe len=8 : set([(3, 2), (2, 1), (4, 3), (2, 2), (2, 4), (1, 0), (3, 4), (0, 3)])
   visited len=8 : set([(0, 1), (1, 2), (1, 3), (3, 3), (1, 4), (0, 2), (2, 3), (1, 1)])
   looking at location = (2, 1)
   call function
#########
#xxx#   #
#x x#   #
#  x#   #
#####   #
#      2#
#########

 * fringe len=9 : set([(3, 2), (3, 1), (2, 0), (4, 3), (2, 2), (2, 4), (1, 0), (3, 4), (0, 3)])
   visited len=9 : set([(0, 1), (1, 2), (1, 3), (3, 3), (1, 4), (0, 2), (2, 3), (2, 1), (1, 1)])
   looking at location = (4, 3)
 * fringe len=8 : set([(3, 2), (3, 1), (2, 0), (2, 2), (2, 4), (1, 0), (3, 4), (0, 3)])
   visited len=10 : set([(0, 1), (1, 2), (1, 3), (3, 3), (1, 4), (0, 2), (2, 3), (2, 1), (4, 3), (1, 1)])
   looking at location = (2, 2)
   call function
#########
#xxx#   #
#xxx#   #
#  x#   #
#####   #
#      2#
#########

 * fringe len=7 : set([(3, 2), (3, 1), (0, 3), (2, 0), (1, 0), (3, 4), (2, 4)])
   visited len=11 : set([(0, 1), (1, 2), (1, 3), (3, 3), (1, 4), (0, 2), (2, 3), (2, 1), (4, 3), (2, 2), (1, 1)])
   looking at location = (3, 2)
   call function
#########
#xxx#   #
#xxx#   #
# xx#   #
#####   #
#      2#
#########

 * fringe len=7 : set([(3, 1), (0, 3), (2, 0), (4, 2), (1, 0), (3, 4), (2, 4)])
   visited len=12 : set([(0, 1), (1, 2), (3, 2), (1, 3), (3, 3), (1, 4), (0, 2), (2, 3), (2, 1), (4, 3), (2, 2), (1, 1)])
   looking at location = (3, 1)
   call function
#########
#xxx#   #
#xxx#   #
#xxx#   #
#####   #
#      2#
#########

 * fringe len=8 : set([(3, 0), (4, 1), (0, 3), (2, 0), (4, 2), (1, 0), (3, 4), (2, 4)])
   visited len=13 : set([(0, 1), (1, 2), (3, 2), (1, 3), (3, 3), (3, 1), (1, 4), (0, 2), (2, 3), (2, 1), (4, 3), (2, 2), (1, 1)])
   looking at location = (0, 3)
 * fringe len=7 : set([(3, 0), (4, 1), (2, 0), (4, 2), (1, 0), (3, 4), (2, 4)])
   visited len=14 : set([(0, 1), (1, 2), (3, 2), (1, 3), (3, 3), (3, 1), (1, 4), (0, 2), (2, 3), (2, 1), (4, 3), (2, 2), (0, 3), (1, 1)])
   looking at location = (2, 0)
 * fringe len=6 : set([(3, 0), (4, 1), (4, 2), (1, 0), (3, 4), (2, 4)])
   visited len=15 : set([(0, 1), (1, 2), (3, 2), (1, 3), (3, 3), (3, 1), (1, 4), (0, 2), (2, 0), (2, 3), (2, 1), (4, 3), (2, 2), (0, 3), (1, 1)])
   looking at location = (4, 2)
 * fringe len=5 : set([(3, 0), (4, 1), (1, 0), (3, 4), (2, 4)])
   visited len=16 : set([(0, 1), (1, 2), (3, 2), (1, 3), (3, 3), (3, 1), (1, 4), (0, 2), (2, 0), (2, 3), (2, 1), (4, 3), (2, 2), (4, 2), (0, 3), (1, 1)])
   looking at location = (1, 0)
 * fringe len=4 : set([(3, 0), (4, 1), (3, 4), (2, 4)])
   visited len=17 : set([(0, 1), (1, 2), (3, 2), (1, 3), (3, 3), (3, 1), (1, 4), (0, 2), (2, 0), (2, 3), (2, 1), (4, 3), (2, 2), (1, 0), (4, 2), (0, 3), (1, 1)])
   looking at location = (3, 4)
 * fringe len=3 : set([(3, 0), (4, 1), (2, 4)])
   visited len=18 : set([(0, 1), (1, 2), (3, 2), (1, 3), (3, 3), (3, 1), (1, 4), (0, 2), (2, 0), (2, 3), (2, 1), (4, 3), (2, 2), (1, 0), (4, 2), (0, 3), (3, 4), (1, 1)])
   looking at location = (2, 4)
 * fringe len=2 : set([(3, 0), (4, 1)])
   visited len=19 : set([(0, 1), (1, 2), (3, 2), (1, 3), (3, 3), (3, 1), (2, 4), (1, 4), (0, 2), (2, 0), (2, 3), (2, 1), (4, 3), (2, 2), (1, 0), (4, 2), (0, 3), (3, 4), (1, 1)])
   looking at location = (3, 0)
 * fringe len=1 : set([(4, 1)])
   visited len=20 : set([(0, 1), (1, 2), (3, 2), (1, 3), (3, 3), (3, 0), (3, 1), (2, 4), (1, 4), (0, 2), (2, 0), (2, 3), (2, 1), (4, 3), (2, 2), (1, 0), (4, 2), (0, 3), (3, 4), (1, 1)])
   looking at location = (4, 1)
>>>
"""
