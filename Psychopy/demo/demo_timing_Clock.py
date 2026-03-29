#!/usr/bin/env python3
#
# Description:
# core.Clock()
# A convenient class to keep track of time in your experiments. 
# You can have as many independent clocks as you like

# import packages
from psychopy import visual, core

# Setup stimulus
win = visual.Window([800, 600])
gabor = visual.GratingStim(win, tex='sin', mask='gauss', sf=5, name='gabor')
gabor.autoDraw = True  # Automatically draw every frame
gabor.autoLog = False  # Or we'll get many messages about phase change

# Let's draw a stimulus for 5 s, drifting for middle 2.5 s
clock = core.Clock() # set up a clock
while clock.getTime() < 5.0:  # Clock times are in seconds
    if 0.5 <= clock.getTime() < 3.0:
        gabor.phase += 0.1  # Increment by 10th of cycle
    win.flip()
    
core.quit()
win.close()