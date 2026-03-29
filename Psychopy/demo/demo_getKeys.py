#!/usr/bin/env python3
#
# Description:
# difference between functions of getKeys and waitKeys
# getKeys: Returns a list of keys that were pressed.
# waitKeys: Same as ~psychopy.event.getKeys, but halts everything 
#           (including drawing) while awaiting input from keyboard.

from psychopy import visual, core, event, monitors

# Set up the monitor parameters, so we can use 'deg' as the screen units
mon = monitors.Monitor("mac15", distance=57.0, width=32.0)
mon.setSizePix([1440, 900])

# create a window to draw in
win = visual.Window([800, 600], monitor=mon, units="deg")

# INITIALISE SOME STIMULI
gabor = visual.GratingStim(win, tex="sin", mask="gauss", size=6.0, ori=45.0)
message = visual.TextStim(win, pos=(0.0, 5.0), text='Hit Q or ESC to quit')
trialClock = core.Clock()

# repeat drawing for each frame
while trialClock.getTime(): 
    # Draw the Gabor on screen
    gabor.draw()
    message.draw()
    win.flip()

    # Update the phase of the Gabor following each screen refresh
    gabor.phase += 0.05
    
    # handle key presses each frame
#    if event.waitKeys(keyList=['escape', 'q']): # static grating
    if event.getKeys(keyList=['escape', 'q']): # moving grating
        win.close()
        core.quit()

win.close()
core.quit()