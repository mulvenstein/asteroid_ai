import pyautogui                # move mouse
import random                   # randomly choosing moves
import sys, os                  # appending path of game_files
import subprocess               # run instace of asteroids game in background.
import time                     # testing gen 0 running for 10 seconds
import ctypes                   # sending Virtual Keyboard presses
from ctypes import wintypes     # sending Virtual Keyboard presses
from multiprocessing import Process,Queue,Pipe, freeze_support
                                # shared data to determine loss or not
sys.path.append(os.path.join(sys.path[0],"game_files"))
from game import play

user32 = ctypes.WinDLL('user32', use_last_error=True)
INPUT_MOUSE    = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
KEYEVENTF_SCANCODE    = 0x0008
MAPVK_VK_TO_VSC = 0
# msdn.microsoft.com/en-us/library/dd375731
VK_TAB  = 0x09
VK_MENU = 0x12
VK_SPACE = 0x20
VK_Q = 0x51
VK_R = 0x52
VK_UP = 0x25
VK_LEFT = 0x26
VK_RIGHT = 0x27
VK_W = 0x57
VK_A = 0x41
VK_D = 0x44

# C struct definitions

wintypes.ULONG_PTR = wintypes.WPARAM
class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))
    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)
class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))
class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))

LPINPUT = ctypes.POINTER(INPUT)

def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args

user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT, # nInputs
                             LPINPUT,       # pInputs
                             ctypes.c_int)  # cbSize

def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def press(virtual_key):
    print("trying " + str(virtual_key))
    PressKey(virtual_key)
    time.sleep(.01)
    ReleaseKey(virtual_key)
    time.sleep(.01) 
# directx scan codes http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
 
# parent_conn,child_conn = Pipe()  # try using multiprocessing
# p = Process(target=f, args=(child_conn,)) 
# p.start()
# print(parent_conn.recv())   # prints "Hello"

# p = subprocess.Popen([sys.executable, 'game_files/main.py'], #try with subprocess
#                                     stdout=subprocess.PIPE, 
#                                     stderr=subprocess.STDOUT)

if __name__ == '__main__':
    freeze_support()

    parent_con,child_con = Pipe()
    p = Process(target=play, args=(child_con,))
    p.start()

    resolution = pyautogui.size()
    pyautogui.moveTo(resolution[0]/2, resolution[1]/2 - 210, 1) # move 2 middle of the screen over 1 sec
    pyautogui.click()

    # cur_time = time.time()
    press(VK_R)
    while True:
        press( random.choice( [VK_A, VK_D, VK_SPACE, VK_W ] ) )
        # print(parent_con.recv())   # prints "Hello"
        # press(VK_SPACE)
        if ( parent_con.recv()=="gg" ):
            print("gg we lose")
            break

    press(VK_Q)