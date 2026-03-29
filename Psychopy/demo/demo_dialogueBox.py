#!/usr/bin/env python3
#
# Description:
# receive data from a dialogue box

from psychopy import visual, core, event, gui

# Get subject info with a dialog
participant = {'Participant ID': '', 'Age': '23', 'Gender': ''}
dlg = gui.DlgFromDict(participant, title='Dialogue Box Exercise', sortKeys=False)
if dlg.OK == False:
    core.quit() # user pressed cancel button

# create a window to draw in
win = visual.Window([800, 600], units="pix", fullscr=False)

# INITIALISE SOME STIMULI
text_msg = visual.TextStim(win, text='message')

while True: 
    text_msg.text = u"Your inputs are: %s\n\nPress q or ESC to quit!" % list(participant.values())
    text_msg.draw()
    win.flip()
    
    if event.getKeys(keyList=['escape', 'q']):
        win.close()
        core.quit()