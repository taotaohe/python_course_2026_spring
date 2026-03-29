#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Demo: print waitKeys data to show what key was pressed at what time
"""

from psychopy import visual, event, core

win = visual.Window(size=[800, 600], units="pix", fullscr=False)

# Display some text:
msg = visual.TextStim(win, text="""Press left or right arrow key!\n
Otherwise it will shutdown in 5 sec""") 
msg.draw()
win.flip()

# wait for key press
clock = core.Clock()
keys = event.waitKeys(maxWait=5, keyList=["left", "right"], timeStamped=clock) # timeStamped=True

print(keys)

win.close()
core.quit()