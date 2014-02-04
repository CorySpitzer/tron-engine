#!/usr/bin/env python
"""
 player.py
 Manage a Tron player.
 Robert Xiao, Jan 31 2010 
 minor edits by Jim Mahoney, Jan 2014
"""
import signal, os, sys, string
from time import clock
from subprocess import Popen, PIPE

P0BOARD = string.maketrans('1\x81\x82\x83\x842\xa1\xa2\xa3\xa4.*\x88\x89\x8a\xa8\xa9\xaa','          ########')
P1BOARD = string.maketrans('1\x81\x82\x83\x842\xa1\xa2\xa3\xa4.*\x88\x89\x8a\xa8\xa9\xaa','1111122222########')
P2BOARD = string.maketrans('1\x81\x82\x83\x842\xa1\xa2\xa3\xa4.*\x88\x89\x8a\xa8\xa9\xaa','2222211111########')

has_alarm = (hasattr(signal, 'SIGALRM') and hasattr(signal, 'alarm'))
if not has_alarm:
    print "Warning: System does not support alarm(); timeouts will not be strictly enforced."

if not hasattr(os, 'kill'):
    try:
        import win32api
    except ImportError:
        print "Warning: System does not support kill(); process may end up spinning upon process exit."
    def kill(pid, sig=signal.SIGTERM):
        # http://www.python.org/doc/faq/windows/
        import win32api
        if sig != signal.SIGTERM:
            raise OSError("Sending any signal except SIGTERM is not supported on Windows.")
        handle = win32api.OpenProcess(1, 0, pid)
        return (0 != win32api.TerminateProcess(handle, 0))
    use_shell = True
else:
    kill = os.kill
    use_shell = True

class TimeoutException(Exception):
    pass

def alarm(*args):
    raise TimeoutException("Time limit exceeded.")

def set_alarm(timeout=1):
    if has_alarm:
        old_alarm=signal.signal(signal.SIGALRM, alarm)
        signal.alarm(timeout)
        return old_alarm
    else:
        return clock() + timeout

def reset_alarm(old_alarm):
    if has_alarm:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_alarm)
    else:
        if clock() > old_alarm:
            raise TimeoutException("Time limit exceeded.")

class PlayerFailedException(Exception):
    def __init__(self, player, msg):
        Exception.__init__(self, player+" failed: "+str(msg))
        self.player = player

""" http://code.activestate.com/recipes/134892/ """
class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

class Player(object):
    MOVES = {'N':'1', 'E':'2', 'S':'3', 'W':'4', 'I':'1', 'J':'4', 'K':'3', 'L':'2'}
    def __init__(self, cmd, name):
        if cmd == '-':
            self.interactive = True
            self.last_move = 'N'
            try:
                self.get_input = _Getch()
            except:
                self.get_input = raw_input
        else:
            self.interactive = False
            self.process = Popen(cmd, shell=use_shell, stdin=PIPE, stdout=PIPE)
        self.name = name

    def readchar(self):
        while True:
            c = self.process.stdout.read(1)
            if c and c.isspace(): continue
            return c

    def readline(self):
        return self.process.stdout.readline()

    def writeline(self, s):
        self.process.stdin.write(s+'\n')
        self.process.stdin.flush()

    def send_eof(self):
        if not self.interactive:
            self.process.stdin.close()

    def getmove(self, board, player):
        try:
            if self.interactive:
                sys.stdout.write("Move (i/j/k/l or n/e/s/w) [%s]? "%self.last_move)
                ret = self.get_input().strip()
                ret = ret[:1].upper()
                if not ret:
                    ret = self.last_move
                else:
                    self.last_move = ret
                if ret in self.MOVES:
                    ret = self.MOVES[ret]
            else:
                self.writeline(board.getdims())
                for l in board.getboard():
                    if player == '1':
                        self.writeline(l.translate(P1BOARD))
                    else:
                        self.writeline(l.translate(P2BOARD))
                old_alarm = set_alarm(timeout=1)
                ret = self.readchar()
                reset_alarm(old_alarm)
            assert ret in '1234', "Player made an invalid move."
            return int(ret)
        except Exception, e:
            raise PlayerFailedException(self.name, e)

    def send_signal(self, sig):
        if self.process.poll() is None:
            try:
                kill(self.process.pid, sig)
            except:
                return False
            return True
        return False

    def sigterm(self):
        if self.interactive:
            return True
        return self.send_signal(signal.SIGTERM)

    def sigkill(self):
        if self.interactive:
            return True
        if hasattr(signal, 'SIGKILL'):
            return self.send_signal(signal.SIGKILL)
        else:
            return self.send_signal(signal.SIGTERM)
