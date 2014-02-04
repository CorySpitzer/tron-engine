"""
 Game logic for Tron game.
 Robert Xiao, Feb 2 2010 

 minor edits by Jim Mahoney, Jan 2014
"""
import random

class Board:
    def __init__(self, w, h, start=None, layout=None, outerwall=True):
        ''' w: width
            h: height
            start:
                "symrand" for symmetrically random (default)
                "random" for totally random
                ((x1,y1), (x2,y2)) to put p1 at (x1,y1) and p2 at (x2,y2)
            layout:
                None to have an empty board
                a list of strings, one per row of the board, which show the initial
                placement of walls and optionally players '''
        self.w = w
        self.h = h
        if layout is not None and start is None:
            p1loc = None
            p2loc = None
            for y,row in enumerate(layout):
                for x,c in enumerate(row):
                    if c == '1':
                        p1loc = (x,y)
                    elif c == '2':
                        p2loc = (x,y)
            if p1loc is None and p2loc is None:
                self.start = "symrand"
            elif p1loc is not None and p2loc is not None:
                self.start = (p1loc, p2loc)
            else:
                raise ValueError("Board is missing a player position!")
        elif start is None:
            self.start = "symrand"
        else:
            self.start = start
        if layout is None:
            self.layout = [' '*w]*h
        else:
            self.layout = layout

        if outerwall:
            self.w += 2
            self.h += 2
            self.layout = ['#'*self.w] + ['#'+row+'#' for row in self.layout] + ['#'*self.w]
            if isinstance(self.start, (tuple, list)):
                p1, p2 = self.start
                self.start = (p1[0]+1, p1[1]+1), (p2[0]+1, p2[1]+1)

def BoardFile(fn):
    f = open(fn, "rU")
    line = f.readline().split()
    w,h = int(line[0]), int(line[1])
    layout = []
    for i in xrange(h):
        layout.append(f.readline().strip('\n'))
    return Board(w, h, layout=layout, outerwall=False)


class GameBoard:
    MOVES = [None, (0, -1), (1, 0), (0, 1), (-1, 0)]
    def __init__(self, template):
        w = self.width = template.w
        h = self.height = template.h
        self.board = map(list, template.layout)
        self.board_trail = [list('-')*w for i in xrange(h)]
        if template.start in ("symrand", "random"):
            free_squares = [(x,y) for x in xrange(w) for y in xrange(h) if self.board[y][x]==' ']
            for i in xrange(10):
                x,y = random.choice(free_squares)
                self.p1loc = x,y
                if template.start == "symrand":
                    self.p2loc = w-1-x, h-1-y
                else:
                    self.p2loc = random.choice(free_squares)
                if self.p1loc != self.p2loc and self.board[self.p1loc[1]][self.p1loc[0]] == ' '\
                                            and self.board[self.p2loc[1]][self.p2loc[0]] == ' ':
                    break
            else:
                raise Exception("Couldn't place players randomly.")
        else:
            self.p1loc, self.p2loc = template.start
        self.start = self.p1loc, self.p2loc
        self.board[self.p1loc[1]][self.p1loc[0]] = '1'
        self.board[self.p2loc[1]][self.p2loc[0]] = '2'
        self.diff = None

    def project(self, pos, delta):
        return pos[0]+delta[0], pos[1]+delta[1]

    def isfree(self, pos):
        return (0 <= pos[0] < self.width and 0 <= pos[1] < self.height) and self.board[pos[1]][pos[0]] == ' '

    def move(self, p1move, p2move):
        p1loc = self.project(self.p1loc, self.MOVES[p1move])
        p2loc = self.project(self.p2loc, self.MOVES[p2move])
        self.board_trail[self.p1loc[1]][self.p1loc[0]] = ' NESW'[p1move]
        self.board_trail[self.p2loc[1]][self.p2loc[0]] = ' NESW'[p2move]
        p1lost = False
        p2lost = False
        if not self.isfree(p1loc):
            p1lost = True
        if not self.isfree(p2loc):
            p2lost = True
        outcome = None
        if (p1lost and p2lost) or p1loc == p2loc:
            outcome = 'D'
            p1move = p2move = 10 # draw
        elif p1lost:
            outcome = '2'
            p1move = 9 # lose
            p2move = 8 # win
        elif p2lost:
            outcome = '1'
            p1move = 8
            p2move = 9

        self.board[self.p1loc[1]][self.p1loc[0]] = '.'
        self.board[self.p2loc[1]][self.p2loc[0]] = '*'
        self.board[p1loc[1]][p1loc[0]] = chr(128+p1move)
        self.board[p2loc[1]][p2loc[0]] = chr(160+p2move)
        self.diff = self.p1loc, self.p2loc, p1loc, p2loc
        self.p1loc = p1loc
        self.p2loc = p2loc
        return outcome

    def getdims(self):
        return '%s %s'%(self.width, self.height)

    def getboard(self):
        return [''.join(row) for row in self.board]
