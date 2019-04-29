---REQUIREMENTS---
using game 
sudo apt-get install  python-xlib
pip3 install pyxel numpy 
---------------

# general notes

0) NN controls ship
1) make player see in 8 directions
   - if object in one of directions, calculate distance
     move tf away from that
2) generations of about 200 players ? 
3) controls are forward, left, right, and shoot (space). 


# implementation stuff
- figure out how to send keyboard commands
--https://stackoverflow.com/questions/13564851/how-to-generate-keyboard-events-in-python ??
  try ctypes (suggested answer) if latency matters.
  For quick and dirty use pyautogui

    from pyautogui import press, typewrite, hotkey

    press('a')
    typewrite('quick brown fox')
    hotkey('ctrl', 'w')
 
  place pointer in middle of the screen then click M1 ?
  1920x1080 mid => 959,539
    pyautogui.moveTo(959,539)
  to click, use pyautogui.click()
    pyautogui.click()  # click the mouse

  https://pyautogui.readthedocs.io/en/latest/keyboard.html # LIST OF KEYBOARD COMMANDS

  pyautogui.press(['up', 'up', 'up'])

- make lines of length X coming out of the ship at 45 deg intervals

