#!/usr/bin/env python
"""
 Play a full Tron tournament.
 Robert Xiao, Jan 31 2010

 Modified Jan 2014 Jim Mahoney :
   * board file format is list of map files, one per line
   * replay option to save visualization files
"""

from sys import stderr
import os

from round import run_round
from player import PlayerFailedException
from board import Board, BoardFile

class Contestant(object):
    def __init__(self, cmd, name, id=0):
        self.cmd = cmd
        self.name = name
        self.id = id
        self.win = self.loss = self.draw = 0
        self.null_loss = self.null_win = 0

def do_round(p1, p2, board, options, replay):
    if options.verbose >= 2:
        print >>stderr, " ", p1.name, p2.name,
    try:
        result = run_round(p1.cmd, p2.cmd, board, p1.name, p2.name,
                           (options.verbose >= 3), ansi=options.ansi,
                           replay=replay)
    except PlayerFailedException, e:
        if e.player == p1.name:
            if options.verbose >= 2:
                print >>stderr, "P1FAILED"
            p1.null_loss += 1
            p2.null_win += 1
        elif e.player == p2.name:
            if options.verbose >= 2:
                print >>stderr, "P2FAILED"
            p2.null_loss += 1
            p1.null_win += 1
        else:
            raise
        return

    assert result in ('12D'), "Round returned bad result."
    if result == '1':
        p1.win += 1
        p2.loss += 1
        if options.verbose >= 2:
            print >>stderr, "P1WIN"
    elif result == '2':
        p2.win += 1
        p1.loss += 1
        if options.verbose >= 2:
            print >>stderr, "P2WIN"
    else:
        p1.draw += 1
        p2.draw += 1
        if options.verbose >= 2:
            print >>stderr, "DRAW"

def run_contest(contestants, boards, options, users=None, boardnames=[]):
    for bi, b in enumerate(boards):
        for r in xrange(options.rounds):
            if options.verbose >= 1:
                print >>stderr, "board '{}'  round {}".format(
                    boardnames[bi], r+1)
            for i in xrange(len(contestants)):
                for j in xrange(len(contestants)):
                    if i==j:
                        # playing a bot against itself is uninteresting
                        continue
                    if users and contestants[i].id not in users:
                        # require that, when playing a partial tournament,
                        # that the user's bot is consistently first player.
                        continue
                    if options.replay:
                        replay = "{}/{}__{}__{}__{}.tron".format(
                            options.replay, boardnames[bi],
                            contestants[i].name, contestants[j].name, r+1)
                    else:
                        replay = False
                    do_round(contestants[i], contestants[j], b,
                             options, replay=replay)

if __name__ == '__main__':
    import sys
    from optparse import OptionParser

    parser = OptionParser(usage="usage: %prog [options] <bot-list> <board-list>")
    parser.add_option("-v", "--verbose", action="count", dest="verbose",
                      default=0, help="Be verbose; additional -v increase verbosity.")
    parser.add_option("-q", "--quiet", action="store_const", const=0, dest="verbose",
                      help="Print only the game summary without additional information.")
    parser.add_option("-r", "--rounds", action="store", type="int", dest="rounds",
                      default=1, help="Number of rounds that each pair of bots play per board")
    parser.add_option("-u", "--user", action="append", type="int", dest="users",
                      help="If specified, these bot IDs will participate in every match.")
    parser.add_option("--no-color", action="store_false", dest="ansi",
                      default=True, help="Disable colour support.")

    parser.add_option("--replay", action="store", type="string",
                      dest="replay", help="replay folder", default="")

    (options, args) = parser.parse_args()

    if len(args) == 0:
        # Interactive mode selection.
        import atexit
        def onquit():
            raw_input("Press <enter> to exit.")
        atexit.register(onquit)
        try:
            f=open("tournament_default.txt", "r")
            f1=f.readline().strip()
            f2=f.readline().strip()
            verbose=f.readline().strip()
            f.close()
        except:
            f1 = 'samplebotlist.txt'
            f2 = 'sampleboardlist.txt'
            verbose = '3'
        print "Tournament configuration:"
        print "Press <enter> to accept defaults in [brackets]."
        def get_input(prompt, default):
            inp = raw_input(prompt + ' [%s]? '%default)
            if not inp:
                return default
            return inp
        f1 = get_input("Bot list", f1)
        f2 = get_input("Board list", f2)
        print "Detail options:"
        print "0) No output except final standings"
        print "1) Show rounds"
        print "2) Show each match result"
        print "3) Show each move as it is played"
        verbose = get_input("Detail level", verbose)
        
        args = [f1, f2]
        options.verbose = int(verbose)
        try:
            f=open("tournament_default.txt", "w")
            print >> f, f1
            print >> f, f2
            print >> f, verbose
            f.close()
        except Exception, e:
            print "Warning: defaults weren't saved:", e
            raw_input("Press <enter> to continue")

    if len(args) < 2:
        parser.error("Required arguments bot-list and board-list missing.")

    scriptfn = args[0]
    contestants = []
    for line in file(scriptfn, "rt"):
        line = line.split('#')[0].strip()
        if not line:
            continue
        user, name, cmd = line.split(',')
        contestants.append(Contestant(cmd, name, int(user)))

    # -- OLD FILE FORMAT : python code --
    #boards = eval(file(args[1],'r').read())  
    # -- NEW FILE FORMAT : list of map files; # for comment lines --
    boardpaths = filter(lambda x: x[0] != '#',
                        map(lambda x: x.rstrip(),
                            open(args[1], 'r').readlines()))
    # path is e.g. '../../maps/empty_room.txt'; name is e.g. 'empty_room'
    boardnames = map(lambda x: os.path.basename(x)[:-4], boardpaths)
    boards = map(lambda f: BoardFile(f), boardpaths)

    #print "options = {}".format(options)
    if options.replay:
        # create replay folder if it doesn't exist
        #print "options.replay = {}".format(options.replay)
        dir = os.path.abspath(options.replay)
        #print "dir = {}".format(dir)
        if not os.path.exists(dir):
            os.makedirs(dir)

    run_contest(contestants, boards, options, options.users, boardnames)
    name_max = max(len(c.name) for c in contestants)
    name_max = max(name_max, 4)+2
    fmt = "%-"+str(name_max)+"s%-10s%-10s%-10s%-10s%-10s"
    print fmt%("name","wins","losses","draws","nullwins","nulllosses")

    for c in sorted(contestants, key=lambda c:c.win+c.null_win, reverse=True):
        print fmt%(c.name, c.win+c.null_win, c.loss, c.draw, c.null_win, c.null_loss)
