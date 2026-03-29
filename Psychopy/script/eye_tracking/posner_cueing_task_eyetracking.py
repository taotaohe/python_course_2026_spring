#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The experiment script was used to test the ponser cueing task, 
with EYELINK 1000 plus eye-tracker.
"""

## import packages
import random, os, pylink
from psychopy import visual, core, event, gui, monitors
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy

# Get subject info with a dialog
participant = {'subject ID': '', 'subject Initials': ''}
dlg = gui.DlgFromDict(participant, title='Enter participant info here', sortKeys=False)
if dlg.OK == False:
    core.quit() # user pressed cancel button
    
#### Now start using Eyelink in our experiment ############################
# Step 1: Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')
if not tk:
    print("EL is None")
    sys.exit()

# Step 2: Initialize eyelink data files on the Host
if not os.path.exists('edfData'): os.mkdir('edfData')
edfFileName = participant['subject ID'] + '_' + participant['subject Initials'] + '_' + participant['session'] + '.EDF'
tk.openDataFile(edfFileName)

# Step 3: Set up tracking parameters
# clear event buffer and set tracker offline before we change its parameters
pylink.flushGetkeyQueue()
tk.setOfflineMode()

# Get the software version:  1-EyeLink I, 2-EyeLink II, 3/4-EyeLink 1000,
# 5-EyeLink 1000 Plus, 6-Portable DUO
vstr = tk.getTrackerVersionString()
eyelink_ver = int(vstr.split()[-1].split('.')[0])
# print out some version info in the shell
print('Running experiment on %s, version %d' % (vstr, eyelink_ver))

# File and Link data control
# what eye events to save in the EDF file, include everything by default
file_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT'
# what eye events to make available over the link, include everything by default
link_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,FIXUPDATE,INPUT'
# what sample data to save in the EDF data file and to make available
# over the link, include the 'HTARGET' flag to save head target sticker
# data for supported eye trackers
if eyelink_ver > 3:
    file_sample_flags = 'LEFT,RIGHT,GAZE,HREF,RAW,AREA,HTARGET,GAZERES,BUTTON,STATUS,INPUT'
    link_sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,AREA,HTARGET,STATUS,INPUT'
else:
    file_sample_flags = 'LEFT,RIGHT,GAZE,HREF,RAW,AREA,GAZERES,BUTTON,STATUS,INPUT'
    link_sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,INPUT'
tk.sendCommand("file_event_filter = %s" % file_event_flags)
tk.sendCommand("file_sample_data = %s" % file_sample_flags)
tk.sendCommand("link_event_filter = %s" % link_event_flags)
tk.sendCommand("link_sample_data = %s" % link_sample_flags)

# Setup monitor
mon = monitors.Monitor("mac", width=25.0, distance=60.0) 
mon.setSizePix([1440,900])  # pixel size of the full screen
# Open a window 
win = visual.Window((1280, 800), monitor=mon, units="deg", fullscr=False,
                    color=(0,0,0), colorSpace='rgb255')
win.mouseVisible = False

# get the native screen resolution used by PsychoPy
scn_width, scn_height = win.size
# Pass the display pixel coordinates (left, top, right, bottom) to the tracker
# see the EyeLink Installation Guide, "Customizing Screen Settings"
el_coords = "screen_pixel_coords = 0 0 %d %d" % (scn_width - 1, scn_height - 1)
tk.sendCommand(el_coords)
# Write a DISPLAY_COORDS message to the EDF file
# Data Viewer needs this piece of info for proper visualization, see Data
# Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
dv_coords = "DISPLAY_COORDS  0 0 %d %d" % (scn_width - 1, scn_height - 1)
tk.sendMessage(dv_coords)
tk.sendCommand('sample_rate 1000') # sample rate

# Request Pylink to use the PsychoPy window for calibration
graphics = EyeLinkCoreGraphicsPsychoPy(tk, win)
pylink.openGraphicsEx(graphics)


## target position
target_pos = {'left':(-4,0),'right':(4,0)}

## Initilize some stimuli
text_msg = visual.TextStim(win, text='message', font='Songti SC', height=0.8)

# fixation cross
line_h = visual.Line(win, start=(-0.2, 0), end=(0.2, 0), lineWidth=10, colorSpace='rgb255')
line_v = visual.Line(win, start=(0, -0.2), end=(0, 0.2), lineWidth=10, colorSpace='rgb255')
# Rectangle
rect = visual.Rect(win, width=3, height=3, lineColor=(255,255,255), lineWidth=5,
                    fillColor=None, colorSpace='rgb255') 
# polygon
poly = visual.Polygon(win, edges=5, radius=1, fillColor=(255,0,0), 
                        colorSpace='rgb255')

## trial list
trialList = []
for cue in ['cue_left', 'cue_right']:
    for tar in ['tar_left', 'tar_right']:
        if tar == 'tar_left':
            corr_key = 'z'
        else:
            corr_key = 'slash'
        trialList.append([cue, tar, corr_key])
    
## define a function to initialize the data file
def initDataFile(subjInfo):
    """ define a function that initializes the data file and get sub_info"""
    
    if not os.path.exists('csvData'): os.mkdir('csvData')
    fileName = 'csvData/' + subjInfo['subject ID'] + '_' + subjInfo['subject Initials'] + '.csv'
    dataFile = open(fileName, 'w')
    header   = ['subjID', 'subjName', 'cue_pos', 'target_pos', 'corr_key', 
                'tar_onset', 'resp_key', 'resp_time', 'mode']
    dataFile.write(','.join(header) + '\n')
    return dataFile

## add global keys to close the window at any time
def quit_func():
    text_msg.text = u"按下q或ESC键退出实验！"
    text_msg.draw()
    win.flip()
    core.wait(2)
    
    win.close()
    core.quit()
    
## define the run trial
def runTrial(trial_pars, data_file, subjInfo, mode):
    """
    run a single trial.
    
    trial_pars: cue position, target position, and correct response key
    data_file: a file to save the trial data
    subjInfo: information about subject that saved in a dictionnary
    mode: trial mode, practice or test
    
    """
    
    ## Unpacking the parameter list
    cue_pos, tar_pos, corr_key = trial_pars
    

    # get a reference to the currently active EyeLink connection
    el_tracker = pylink.getEYELINK()
    # put the tracker in the offline mode first
    el_tracker.setOfflineMode()

    # Always send a TRIALID message before starting to record
    msg = "TRIALID: %s %s %s %s" % (cue_pos, tar_pos, corr_key, mode)
    el_tracker.sendMessage(msg)
    # record_status_message : show some info on the Host PC
    # here we show how many trial has been tested
    # status_msg = 'TRIAL number %d / %d' % (successTrialN, totalTrialN)
    # el_tracker.sendCommand("record_status_message '%s'" % status_msg)

    # drift-check and re-do camera setup if ESCAPE is pressed
    try:
        error = el_tracker.doDriftCorrect(int(scn_width/2.0),
                                          int(scn_height/2.0), 1, 1) 
        if error is pylink.ESC_KEY:
            el_tracker.doTrackerSetup()
    except:
        el_tracker.doTrackerSetup()

    # put tracker in idle/offline mode before recording
    el_tracker.setOfflineMode()


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
    el_tracker.sendMessage('fix_onset')
    core.wait(1)
    
    ## let's present a cue
    if cue_pos == 'cue_left':
        line_h.setStart((-0.4,0))
    elif cue_pos == 'cue_right':
        line_h.setEnd((0.4,0))
    line_h.draw()
    line_v.draw()    
    
    rect.setPos(target_pos['left'])
    rect.draw()
    rect.setPos(target_pos['right'])
    rect.draw()
    
    win.flip()
    el_tracker.sendMessage('cue_onset')
    core.wait(0.25)
    
    ## let's present a blank between the cue and target
    # remeber to restore the line
    line_h.setStart((-0.2,0))
    line_h.setEnd((0.2,0))
    line_h.draw()
    line_v.draw()    
    
    rect.setPos(target_pos['left'])
    rect.draw()
    rect.setPos(target_pos['right'])
    rect.draw()
    
    win.flip()
    el_tracker.sendMessage('blank_onset')
    core.wait(0.2)
    
    ## let's present the target
    if tar_pos == 'tar_left':
        poly.setPos(target_pos['left'])
    elif tar_pos == 'tar_right':
        poly.setPos(target_pos['right'])
    poly.draw()

    line_h.draw()
    line_v.draw()    
    
    rect.setPos(target_pos['left'])
    rect.draw()
    rect.setPos(target_pos['right'])
    rect.draw()
    
    win.flip()
    el_tracker.sendMessage('target_onset')
    tar_onset = core.getTime()
    core.wait(0.05)
    
    ## wait for a key response
    line_h.draw()
    line_v.draw()    
    
    rect.setPos(target_pos['left'])
    rect.draw()
    rect.setPos(target_pos['right'])
    rect.draw()
    
    win.flip()
    tar_resp = event.waitKeys(2.95, ['z', 'slash'], timeStamped=True)
    
    ## give a feedback
    if tar_resp != None:
        resp_key = tar_resp[0][0] # index the resp key if key is pressed
        
        if resp_key == corr_key:
            line_h.setColor((0,255,0)) # green
            line_v.setColor((0,255,0)) # green
        else:
            line_h.setColor((255,0,0)) # red
            line_v.setColor((255,0,0)) # red
    else: # no response key
        line_h.setColor((255,0,0)) # red
        line_v.setColor((255,0,0)) # red        
    line_h.draw()
    line_v.draw() 
    
    rect.setPos(target_pos['left'])
    rect.draw()
    rect.setPos(target_pos['right'])
    rect.draw()
    
    win.flip()
    core.wait(0.25)
    
    ## write data to file
    if tar_resp != None:
        trial_data = list(subjInfo.values()) + trial_pars + [tar_onset] + \
                     list(tar_resp[0]) + [mode]
    else:
        trial_data = list(subjInfo.values()) + trial_pars + [tar_onset] + \
                     [None, None] + [mode]       
    trial_data = map(str, trial_data)
    data_file.write(','.join(trial_data) + '\n')

    ## clear the screen and set a random ITI
    line_h.setColor((255,255,255))
    line_v.setColor((255,255,255))
    line_h.draw()
    line_v.draw()
    rect.setPos(target_pos['left'])
    rect.draw()
    rect.setPos(target_pos['right'])
    rect.draw() 
    win.flip()
    core.wait(random.choice(range(1000, 2001))*0.001)
    
    ## add global event keys to shutdown the program at any time
    event.globalKeys.clear()
    for key in ['q','escape']:
        event.globalKeys.add(key, func=quit_func)
    
    
## define the run block
def runBlock(mode, DATA_FILE, SUBJ_INFO):
    # prepare the trials
    if mode == 'prac': testList = trialList[:]   # 4 prac trials
    if mode == 'test': testList = trialList[:]*2 # 8 test trials
    random.shuffle(testList)

    trialCount = 0
    successNum = 1
    totalNum = len(testList)
    if(tk.isConnected() and not tk.breakPressed()):
        for pars in testList:
            # do a camera setup/calibration after every N trial
            if trialCount % 100 == 0:
                text_msg.text = u'请告知主试来校准仪器！'
                text_msg.draw()
                win.flip()
                event.waitKeys(keyList=['return'])
                tk.doTrackerSetup()
                
            trialOK = runTrial(pars, DATA_FILE, SUBJ_INFO, mode, successNum, totalNum)
            # recyle the trial if not OK
            if not trialOK: testList.append(pars); successNum -= 1
            successNum += 1
            trialCount += 1

    
## ---------- Real experiment starts from here ----------##
    
## open a data file for saving the data
data_file = initDataFile(participant)

## Hiden the mouse cursor
event.Mouse(visible=False) # will use win by default

## Present the task instruction
# let's flip one frame at first to solve the non full scr problem, 
# not sure the specific reason now.
win.flip()

text_msg.text = u"红色五边形出现在左侧时按z键，\n出现在右侧时按/键。\n\n按空格键开始实验！"
text_msg.draw()
win.flip()
event.waitKeys(keyList=['space'])

# run practice trials
runBlock('prac', data_file, participant)
# practice ends here, give a message to the participant
text_msg.text = u"练习结束, 按空格键开始正式实验!"
text_msg.draw()
win.flip()
event.waitKeys(keyList=['space'])
# run main test trials
runBlock('test', data_file, participant)

# exit the program elegantly
text_msg.text = u"实验结束，感谢您的参与！"
text_msg.draw()
win.flip()
if tk != None:
    # File transfer and cleanup!
    tk.setOfflineMode()
    core.wait(0.5)
    # Close the file and transfer it to Display PC
    tk.closeDataFile()
    tk.receiveDataFile(edfFileName, 'edfData/' + edfFileName)
    tk.close()

## close the window
data_file.close()
win.close()
core.quit()