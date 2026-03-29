#!/usr/bin/env python3
#
# Description:
# The most precise way to control stimulus timing 
# is to present them for a specified number of frames.

# import modules
from psychopy import visual, core

# Setup stimulus
win = visual.Window([800, 600])
gabor = visual.GratingStim(win, tex='sin', mask='gauss', sf=5,
    name='gabor', autoLog=False)

# Let's draw a stimulus for 200 frames, drifting for frames 50:100
for frameN in range(500):   # For exactly 200 frames
    if frameN < 50 or frameN >=300:
        gabor.draw()
    if 50 <= frameN < 300:  # Present stim for a different subset
        gabor.phase += 0.1  # Increment by 10th of cycle
        gabor.draw()
    win.flip()
    
core.quit()
win.close()