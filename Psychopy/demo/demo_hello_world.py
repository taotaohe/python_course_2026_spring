#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demo: show a very basic program: hello world!

"""

# Import key parts of the PsychoPy library:
from psychopy import visual, core

# Create a visual window:
win = visual.Window(size=(1024,768), units='pix', fullscr=False, color=(128,128,128), colorSpace='rgb255')

# Create (but not yet display) some text:
msg1 = visual.TextStim(win, text="Hello world!", pos=(0, 50)) 
msg2 = visual.TextStim(win, text=u"你好，世界!",  pos=(0, -50), font='Songti SC')

# Draw the text to the hidden visual buffer:
msg1.draw()
msg2.draw()

# Show the hidden buffer--everything that has been drawn since the last win.flip():
win.flip()

# Wait 3 seconds so people can see the message, then exit gracefully:
core.wait(10)

win.close()
core.quit()