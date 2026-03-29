#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Demo: global event keys
PsychoPy® fully automatically monitors and processes key presses during 
most portions of the experimental run, for example during core.wait() periods, 
or when calling win.flip().
"""

from psychopy import visual, event, core, prefs
prefs.general['audioLib'] = ['pygame']

# Clear any existing global event keys
event.globalKeys.clear()

# Create a visual window:
win = visual.Window(size=(800, 600), fullscr=False)
text_msg = visual.TextStim(win, text=u"按下q或ESC退出程序!", font='Songti SC')

# Define the shutdown function
def quit_func():
    text_msg.text = u"你已按下q或ESC键！"
    text_msg.draw()
    win.flip()
    core.wait(3)
    win.close()
    core.quit()

# Add global keys so that we can shutdown at any time
for key in ['q', 'escape']:
    event.globalKeys.add(key=key, func=quit_func)

print(repr(event.globalKeys))

# Main loop to keep the window open and check for global key events
while True:
    text_msg.draw()
    win.flip()
    if 'a' in event.getKeys():
        break

win.close()
core.quit()



