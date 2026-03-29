#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Demo: show "hello world" successively
"""

from psychopy import visual, core, event

win = visual.Window([800,600])

message = visual.TextStim(win, text='Hello')
message.autoDraw = True  # Automatically draw every frame

win.flip()
core.wait(2.0)

message.text = 'world!'  # Change properties of existing stim
win.flip()
core.wait(2.0)

# close the window and quit PsychoPy
win.close()
core.quit()