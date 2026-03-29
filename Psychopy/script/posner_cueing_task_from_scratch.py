#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Coder.
The script was used to measure posner cueing task.
"""

## --- Import packages --- ##
import random
from psychopy import visual, core, event, gui

## Open a window 
win = visual.Window((1280, 800), units='pix', fullscr=False, color='black')

## Possible target position
target_pos = {'left':(-300, 0), 'right':(300, 0)}

## Initilize some stimuli
text_msg = visual.TextStim(win, text='message', font='Songti SC')
# fixation cross
line_h = visual.Line(win, start=(-20,0), end=(20,0))
line_v = visual.Line(win, start=(0,-20), end=(0,20))
# Rectangle
rect = visual.Rect(win, width=200, height=200, lineColor='gray', fillColor=None) 
# polygon
poly = visual.Polygon(win, edges=5, radius=30, fillColor='red') 

## A trial list includes all possible parameter combinations
trialList = [
    ['cue_left', 'tar_left', 'z', 'valid'],
    ['cue_left', 'tar_right', 'slash', 'invalid'],
    ['cue_right', 'tar_left', 'z', 'invalid'],
    ['cue_right', 'tar_right', 'slash', 'valid'],
    ]
random.shuffle(trialList)

## Get subject info with a dialog
participant = {'subject ID': '', 'subject Initials': ''}
dlg = gui.DlgFromDict(participant, title='Enter participant info here', sortKeys=False)

## open a data file for saving the data
data_file = open(participant['subject Initials']+'.csv', 'w')

## Present the task instruction
text_msg.text = u"红色五边形出现在左侧时按z键，出现在右侧时按/键。\n\n按空格键开始实验！"
text_msg.draw()
win.flip()
event.waitKeys(keyList=['space'])

## define a trial
for itrial in trialList:
    
    ## Unpacking the parameter list
    cue_pos, tar_pos, correct_key, condition = itrial
    
    ## Now, let's present the first frame on the screen (fixation + squares)
    # draw a fixation cross
    line_h.draw()
    line_v.draw()
    # draw two squares on the left and right sides
    rect.setPos(target_pos['left'])
    rect.draw()
    rect.setPos(target_pos['right'])
    rect.draw()
    # flip the screen and wait for second
    win.flip()
    core.wait(1)
    
    # let's present a cue
    if cue_pos == 'cue_left':
        line_h.setStart((-40,0))
    elif cue_pos == 'cue_right':
        line_h.setEnd((40,0))
    line_h.draw()
    line_v.draw()  
    
    rect.setPos(target_pos['left'])
    rect.draw()
    rect.setPos(target_pos['right'])
    rect.draw()
    
    win.flip()
    core.wait(0.25)
    
    # let's present the target and wait for key
    if tar_pos == 'tar_left':
        poly.setPos(target_pos['left'])
    elif tar_pos == 'tar_right':
        poly.setPos(target_pos['right'])
    poly.draw()
    # remeber to restore the line
    line_h.setStart((-20,0))
    line_h.setEnd((20,0))
    line_h.draw()
    line_v.draw()  
    
    rect.setPos(target_pos['left'])
    rect.draw()
    rect.setPos(target_pos['right'])
    rect.draw()
    
    win.flip()
    tar_onset = core.getTime()
    tar_resp = event.waitKeys(5, ['z', 'slash'], timeStamped=True)
    
    # write data to file
    if tar_resp != None:
        trial_data = itrial + [tar_onset] + list(tar_resp[0])
    else:
        trial_data = itrial + [tar_onset] + [None, None]        
    trial_data = map(str, trial_data)
    data_file.write(','.join(trial_data) + '\n')

    # clear the screen and set an ITI of 1 s
    line_h.draw()
    line_v.draw()    
    rect.setPos(target_pos['left'])
    rect.draw()
    rect.setPos(target_pos['right'])
    rect.draw()
    win.flip()
    core.wait(1)
    
# close the data file
data_file.close()

# exit the program elegantly
text_msg.text = u"实验结束，感谢您的参与！"
text_msg.draw()
win.flip()
core.wait(3)
    
# Close the window and quit PsychoPy
win.close()
core.quit()