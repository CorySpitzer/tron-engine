#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Play one round of Tron.
 Robert Xiao, Jan 31 2010
 Colorization idea cribbed from Jeremy Roman (jbroman).

 ----------

 2014 Jim Mahoney
 tested with python 2.7.5
   * added FPS option and slowed default animation
   * changed "vis" options to "replay"
   * modified replay output to match replay.html and replay.js
   * added winner to replay file format
"""
import sys, re
import colorize as color
from time import sleep, clock
from player import Player, PlayerFailedException, P0BOARD, P1BOARD
from board import Board, GameBoard, BoardFile

class ErrorInRound(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

# Approximate frames-per-second to run the visualization
FPS = 30

# Speedup factor per frame (set to 0 to disable speedup)
# This can make tedious spacefilling games speed up over time
# to make them shorter.
FPS_SPEEDUP = 0.01

CHARS = { '#': '#',
          '.': '.',
          '*': '*',
          '\x81': '1',
          '\x82': '1',
          '\x83': '1',
          '\x84': '1',
          '1': '1',
          '\xa1': '2',
          '\xa2': '2',
          '\xa3': '2',
          '\xa4': '2',
          '2': '2',
          ' ': ' ',
          '\x88': '!',
          '\x89': '@',
          '\x8a': '-',
          '\xa8': '!',
          '\xa9': '@',
          '\xaa': '-'}

RST = color.reset
C1T = color.bg(color.RED)
C2T = color.bg(color.BLUE)
C1 = color.bg(color.RED+color.GREEN)
C2 = color.bg(color.BLUE+color.GREEN)

ANSICHARS = { '#':  (color.inverse, "  "), # game wall
              '.':  (C1T, "  "),           # player 1 trail
              '*':  (C2T, "  "),           # player 2 trail
              '\x81': (C1, '/\\'),         # player 1 directions
              '\x83': (C1, '\\/'),
              '\x84': (C1, '<<'),
              '\x82': (C1, '>>'),
              '1':    (C1, '11'),          # player 1 initial
              '\xa1': (C2, "/\\"),         # player 2 directions
              '\xa3': (C2, "\\/"),
              '\xa4': (C2, "<<"),
              '\xa2': (C2, ">>"),
              '2':    (C2, "22"),          # player 2 initial
              ' ':    (RST, "  "),         # floor (open)
              '\x88': (C1, ':)'),          # player 1 wins
              '\x89': (C1, ':('),          # player 1 loses
              '\x8a': (C1, ':S'),          # player 1 draws
              '\xa8': (C2, ':)'),          # player 2 wins
              '\xa9': (C2, ':('),          # player 2 loses
              '\xaa': (C2, ':S'),}         # player 2 draws

def clear_line(board):
    sys.stdout.write('\r')
    sys.stdout.write(' '*board.width)
    sys.stdout.write('\r')

def legend(headcolor, tailcolor, status, name):
    tailcolor()
    sys.stdout.write('  ')
    headcolor()
    sys.stdout.write(status)
    color.reset()
    sys.stdout.write(' '+name)

def blank_line():
    sys.stdout.write('\r\n')

def print_board(board, name1, name2, ansi=False):
    if ansi:
        if board.diff is None:
            color.clear()
            for line in board.getboard():
                for match in re.finditer('(.)\\1*', line):
                    a, b = ANSICHARS[match.group(1)]
                    a()
                    sys.stdout.write(b*len(match.group(0)))
                    color.reset()
                blank_line()
        else:
            for x,y in board.diff:
                color.movexy(x*2, y)
                a, b = ANSICHARS[board.board[y][x]]
                a()
                sys.stdout.write(b)
                color.reset()
            color.movexy(0, board.height)
        clear_line(board)
        blank_line()
        clear_line(board)
        x, y = board.p1loc
        legend(C1, C1T, ANSICHARS[board.board[y][x]][1], name1)
        blank_line()
        clear_line(board)
        x, y = board.p2loc
        legend(C2, C2T, ANSICHARS[board.board[y][x]][1],name2)
        blank_line()
        clear_line(board)
    else:
        print
        for line in board.getboard():
            for c in line:
                sys.stdout.write(CHARS[c])
            print
        print '-'*board.width

def get_replayfile(fn):
    if fn is None:
        return None
    if fn == '-':
        return sys.stdout
    return open(fn, 'w')
    # except:
    #    raise ErrorInRound("couldn't open output file {}".format(fn))

def run_round(cmd1, cmd2, board, 
              name1="Contestant 1", name2="Contestant 2", 
              verbose=False, interactive=False, ansi=False, replay=False,
              **kwargs):
    delay = 1.0/FPS

    try:
        p1 = Player(cmd1, name1)
    except Exception, e:
        raise PlayerFailedException(name1, "Couldn't start process: "+str(e))

    try:
        p2 = Player(cmd2, name2)
    except Exception, e:
        raise PlayerFailedException(name2, "Couldn't start process: "+str(e))
    
    gameboard = GameBoard(board)

    if replay:
        replayfile = get_replayfile(replay)
        replayfile.write("+OK|{} {}|".format(gameboard.width, gameboard.height))
        for line in gameboard.board:
            replayfile.write(''.join(line).translate(P1BOARD))
            replayfile.write('\n')
        replayfile.write("|{}|{}|".format(name1, name2))

    result = None
    try:
        while True:
            if verbose:
                print_board(gameboard, name1, name2, ansi)
            if interactive:
                raw_input("Press <enter> to continue with the next move.")
            start = clock()
            m1 = p1.getmove(gameboard, '1')
            m2 = p2.getmove(gameboard, '2')
            result = gameboard.move(m1, m2)
            if replay:
                replayfile.write('{}'.format(' NESW'[m1]))
                replayfile.write('{}'.format(' NESW'[m2]))
            total_clock = clock()-start
            if verbose and total_clock < delay:
                sleep(delay - total_clock)
            delay *= 1 - FPS_SPEEDUP
            if result is not None:
                break
    except PlayerFailedException, e:
        raise
    finally:
        if verbose:
            if result == '1':
                print_board(gameboard, name1+' (Winner)', name2, ansi)
            elif result == '2':
                print_board(gameboard, name1, name2+' (Winner)', ansi)
            else:
                print_board(gameboard, name1+' (Draw)', name2+' (Draw)', ansi)

        try:    p1.send_eof()
        except: pass

        try:    p2.send_eof()
        except: pass

        if verbose:
            # Sleep another little while to keep the game board on-screen.
            sleep(0.5)
        sleep(0.1)
        if p1.sigterm() or p2.sigterm():
            # one of the processes wasn't quit yet
            sleep(0.25)
            p1.sigkill()
            p2.sigkill()

    if replay:
        # result is winner, '1', '2', or 'D'        
        replayfile.write("|{}|+OK\n".format(result))   
        replayfile.close()

    return result

if __name__ == '__main__':
    import sys
    from optparse import OptionParser

    parser = OptionParser(usage="usage: %prog [options] <cmd1> <cmd2>\ncmd1 " +
                                "and/or cmd2 can be - to indicate a human player.")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                      default=False, help="Show each move as it is played.")
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose",
                      help="Print only the game summary without additional information.")
    parser.add_option("-i", "--interactive", action="store_true", dest="interactive",
                      default=False, help="Pause between moves.")
    parser.add_option("-b", "--board", action="store", dest="board", default=None,
                      help="Board specification (default: Board(10,10) for a 10x10 board)")
    parser.add_option("-B", "--board-file", action="store", dest="boardfile",
                      default=None, help="Board filename")
    parser.add_option("--no-color", action="store_false", dest="ansi",
                      default=True, help="Disable colour support.")
    parser.add_option("--replay", action="store", dest="replay", default=None,
                      help="Store data for javascript replay.html to specified " +
                           "filename (- for stdout)")
    parser.add_option("--FPS", action="store", dest="FPS",
                      default=30, help="animation frames per second (default 30)")
    (options, args) = parser.parse_args()

    try:
        FPS = int(options.FPS)
    except:
        pass

    if options.board and options.boardfile:
        parser.error("-b and -B are mutually exclusive.")

    if options.board:
        options.board = eval(options.board)
    elif options.boardfile:
        options.board = BoardFile(options.boardfile)

    if len(args) == 0:
        # Interactive mode selection.
        import atexit
        def onquit():
            raw_input("Press <enter> to exit.")
        atexit.register(onquit)
        try:
            f=open("round_default.txt", "r")
            c1=f.readline().strip()
            c2=f.readline().strip()
            wh=f.readline().strip()
            f.close()
        except:
            c1 = '-'
            c2 = '-'
            wh = '10,10'
        print "Round configuration:"
        print "Press <enter> to accept defaults in [brackets]."
        print "Use - (a single minus sign) to denote a human player."
        def get_input(prompt, default):
            inp = raw_input(prompt + ' [%s]? '%default)
            if not inp:
                return default
            return inp
        c1 = get_input("Player 1 (red)", c1)
        c2 = get_input("Player 2 (blue)", c2)
        if not options.board:
            wh = get_input("Board size (width, height) or board filename", wh)
        
        args = [c1, c2]
        if not options.board:
            try:
                options.board = eval("Board(%s)"%wh)
            except:
                options.board = BoardFile(wh)
        try:
            f=open("round_default.txt", "w")
            print >> f, c1
            print >> f, c2
            print >> f, wh
            f.close()
        except Exception, e:
            print "Warning: defaults weren't saved:", e
            raw_input("Press <enter> to continue")

    if options.board is None:
        options.board = Board(10, 10)

    if len(args) > 2:
        parser.error("Too many arguments; expected two.")
    if len(args) < 2:
        parser.error("Too few arguments; expected two.")

    cmd1 = args[0]
    cmd2 = args[1]

    if '-' in args:
        # Having a human player implies verbose, to show the board every time.
        options.verbose = True

    if cmd1 == '-':
        name1 = 'Human'
    else:
        name1 = cmd1
    
    if cmd2 == '-':
        name2 = 'Human'
    else:
        name2 = cmd2

    if name1 == name2:
        name1 += ' 1'
        name2 += ' 2'

    outcome = run_round(cmd1, cmd2, name1=name1, name2=name2, **options.__dict__)
    print "outcome:",
    if outcome == '1':
        print "Player 1 wins"
    elif outcome == '2':
        print "Player 2 wins"
    else:
        print "Draw"
