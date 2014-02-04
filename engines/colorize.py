''' Simple multiplatform console colour library.

Robert Xiao, Feb 2 2010 '''

try:
    # Windows colors
    from ctypes import *
    kernel32 = windll.kernel32
    RED = 4
    GREEN = 2
    BLUE = 1
    BRIGHT = 8
    FG_MASK = 15
    BG_MASK = FG_MASK << 4

    class COORD(Structure):
        _fields_ = [("x", c_short),
                    ("y", c_short)]
    class SMALL_RECT(Structure):
        _fields_ = [("topleft", COORD),
                    ("bottomright", COORD)]
    class CONSOLE_SCREEN_BUFFER_INFO(Structure):
        _fields_ = [("size", COORD),
                    ("cursor_pos", COORD),
                    ("attributes", c_int),
                    ("window", SMALL_RECT),
                    ("max_window_size", COORD)]
    STDOUT_HANDLE = kernel32.GetStdHandle(-11) # STD_OUTPUT_HANDLE = -11
    def _get_attribs():
        buf = CONSOLE_SCREEN_BUFFER_INFO()
        assert kernel32.GetConsoleScreenBufferInfo(STDOUT_HANDLE, byref(buf)), "GetConsoleScreenBufferInfo failed."
        return buf.attributes
    DEFAULT_ATTRIBS = _get_attribs()
    def _send(attribs):
        assert kernel32.SetConsoleTextAttribute(STDOUT_HANDLE, attribs), "SetConsoleTextAttribute failed."
    def reset():
        _send(DEFAULT_ATTRIBS)
    def set_fg(color):
        attribs = _get_attribs()
        _send((attribs & ~FG_MASK) | color)
    def set_bg(color):
        attribs = _get_attribs()
        _send((attribs & ~BG_MASK) | (color << 4))
    def inverse():
        attribs = _get_attribs()
        bgc = (attribs & BG_MASK) >> 4
        fgc = (attribs & FG_MASK)
        _send((attribs & ~BG_MASK & ~FG_MASK) | bgc | (fgc << 4))
    def movexy(x,y):
        kernel32.SetConsoleCursorPosition(STDOUT_HANDLE, COORD(x, y))

    import os
    def clear():
        os.system("cls")
except:
    # ANSI colors
    RED = 1
    GREEN = 2
    BLUE = 4
    BRIGHT = 60

    ESC = '\033['
    import sys
    def _send(cmd):
        sys.stdout.write(ESC)
        sys.stdout.write(cmd)
    def reset():
        _send('0m')
    def set_fg(color):
        _send('1;%im'%(color+30))
    def set_bg(color):
        _send('1;%im'%(color+40))
    def movexy(x,y):
        _send('%i;%iH'%(y+1, x+1))
    def inverse():
        _send('7m')
    def clear():
        _send('2J')  # clear screen
        movexy(0,0)  # move to top left

BLACK = 0
YELLOW = RED+GREEN
MAGENTA = RED+BLUE
CYAN = GREEN+BLUE
WHITE = RED+GREEN+BLUE

def bg(color):
    return lambda: set_bg(color)

def fg(color):
    return lambda: set_fg(color)
