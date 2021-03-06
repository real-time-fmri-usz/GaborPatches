#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from psychopy import  gui, visual, core, data, event, logging,parallel
from time import strftime
from random import choice
from numpy.random import choice as choice2
from numpy.random import random
import random as rd
import numpy as np
import csv

##### SETUP #####
#### CHECK TIMING
### Parameters ###

###### EDIT PARAMETERS BELOW #######

stim_dur = 2.     # time in seconds that the subliminal stim appears on the screen [strong,weak,catch]
response_dur = 2.   #Check this in matlab script: how long are stimuli presented there?
stim_size = 256
iti_dur = 0.5
response_keys = {'left':'b','right':'z'}     # keys to use for a left response and a right response
response_keys_inv = {v: k for k, v in response_keys.items()}
reskeys_list = ['b','z']
pix_size = .001

practice_iti_dur = 2
practice_stim_dur = 1.5

#Design stuff
nr_blocks = 14
nr_trial_per_block = 6
duration_rest = 9

###### STOP EDITING BELOW THIS LINE #######

## ParallelPort

port = parallel.ParallelPort()


#Experimenter input
dlg = gui.Dlg(title = 'Experiment Parameters')
dlg.addField('Subject ID:')
dlg.addField('Session:')
dlg.addField('Scanner', choices = ['yes','no'])
dlg.addField('Practice', choices = ['yes','no'])
dlg.addField('Opacity:')
exp_input = dlg.show()

subid = exp_input[0]
session = exp_input[1]
if exp_input[2] == 'yes':
	scanner = True
else:
	scanner = False
if exp_input[3] == 'yes':
	show_practice = True
else:
	show_practice = False

gabor_opacity = float(exp_input[4])
control_opacity = float(0.8)

### Create Block trial_order

block_type = ['gabor', 'control']
rev_block_type = block_type[::-1]
#Create two different block orders
subid = '2'
block_order = ['a'] * nr_blocks
if float(subid) % 2 != 0.0:
    block_order = block_type * int((nr_blocks/len(block_type)))
else:
    block_order = rev_block_type * int((nr_blocks/len(block_type)))



### Visuals ###

#window
win = visual.Window(size=[800, 600],  screen = 0, fullscr = False, units = 'pix')
win.setMouseVisible(False)

#Gabor PARAMETERS

X = stim_size; # width of gabor patch in pixels

sf = 10 / X; # cycles per pixel
left = 357; #left angle in deg
right = 3; #right angle in deg
noiseTexture = random([X,X])*2.0-1. # a X-by-X array of random numbers in [-1,1]

noiseTexture_example = random([256,256])*2.0-1. # a X-by-X array of random numbers in [-1,1]

n_example = visual.GratingStim(
    win = win, mask='gauss', tex = noiseTexture_example,
    size = 256, contrast = 1.0, opacity = 1.0,
)


# noise patch
noise = visual.GratingStim(
    win = win, mask='gauss', tex = noiseTexture,
    size = X, contrast = 1.0, opacity = 1.0,
)

# Fixation Cross
fixation = visual.ShapeStim(
    win=win, name='polygon', vertices='cross',
    size=(20, 20),
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)

fixation_green = visual.ShapeStim(
    win=win, name='polygon', vertices='cross',
    size=(20, 20),
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[0,1,0], fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)


gabor_tex_example_left = (
		    visual.filters.makeGrating(res=256, cycles=256 * sf, ori = 357, gratType = "sin" ) *
		    visual.filters.makeMask(matrixSize=256, shape="gauss", range=[0, 1])
		)


gabor_tex_example_right = (
		    visual.filters.makeGrating(res=256, cycles=256 * sf, ori = 3, gratType = "sin" ) *
		    visual.filters.makeMask(matrixSize=256, shape="gauss", range=[0, 1])
		)


			# signal grating patch
gabor_left_example_vis = visual.GratingStim(win = win, tex = gabor_tex_example_left, mask = None, units = 'pix',  size = 256, contrast = 1.0, opacity = 1, pos= (-200,-100.0))

gabor_right_example_vis = visual.GratingStim(win = win, tex = gabor_tex_example_right, mask = None, units = 'pix',  size = 256, contrast = 1.0, opacity = 1, pos= (200,-100.0))

gabor_left_example = visual.GratingStim(win = win, tex = gabor_tex_example_left, mask = None, units = 'pix',  size = 256, contrast = 1.0, opacity = .8)

gabor_right_example = visual.GratingStim(win = win, tex = gabor_tex_example_right, mask = None, units = 'pix',  size = 256, contrast = 1.0, opacity = .8)

###text
#headers
instructions_header = visual.TextStim(win, text='INSTRUCTIONS', color = 'black', alignHoriz = 'center', alignVert = 'top', pos = (0.0,250.))
experiment_header = visual.TextStim(win, text='MAIN EXPERIMENT', color = 'black', alignHoriz = 'center',  alignVert = 'top', pos = (0.0,0.0))

#Left
left_text = visual.TextStim(win, text='LEFT', color = 'black', alignHoriz = 'center', alignVert = 'top', pos = (-200.0,100))
right_text = visual.TextStim(win, text='RIGHT', color = 'black', alignHoriz = 'center', alignVert = 'top', pos = (200.0,100))

#instructions
instructions_text1 = visual.TextStim(win, text='In each trial of this experiment angled black and white stripes will appear in the middle of the screen', color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,0.0))
instructions_text2 = visual.TextStim(win, text='The stripes will be angled to the left or to the right', color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,160.0))


instructions_text5 = visual.TextStim(win, text='Press the "%s" key if the stripes are angled to the %s side.'%(response_keys['left'],'left'), color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,50.0))
instructions_text6 = visual.TextStim(win, text='Press the "%s" key if if the stripes are angled to the %s side.'%(response_keys['right'],'right'),  color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,-50))



instructions2_text = visual.TextStim(win, text='Geat job! Make sense?',  color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,0.1))



#mis
example_text = visual.TextStim(win, text='Here are some practice examples . . .',  color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,0.0))
get_ready_text = visual.TextStim(win, text='Now let\'s move on the the real experiment.', color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,0.0))
press_left_text = visual.TextStim(win, text='Press the "%s" key'%response_keys['left'], color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,-200.))
press_right_text = visual.TextStim(win, text='Press the "%s" key'%response_keys['right'], color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,-200))

### Timing ###

practice_clock = core.Clock()
experiment_clock = core.Clock()

### Results Logging ###
time_stamp = strftime('%d-%m-%Y_%H:%M:%S').replace(':','_')
output_file_path = 'results/%s_%s_%s.csv'%(subid,session,time_stamp)
output_file = open(output_file_path,'w+')

###TO DO
output_file.write('trial,trial_type,response,correct,response_time,cumulative_response_time,trial_time,stim_onset,stim_dur,opacity\n')
output_file.flush()


### Quitting ###
event.globalKeys.clear()
quit_key = 'q'
def quit_experiment():
	core.quit()
event.globalKeys.add(key=quit_key, func=quit_experiment)


##### RUN EXPERIMENT #####

###  instructions  ###
#explain task
if show_practice:
	#intro to experiment
	instructions_header.draw()
	instructions_text1.draw()
	win.flip()
	event.waitKeys(keyList='space')
	instructions_text2.draw()
	gabor_left_example_vis.draw()
	left_text.draw()
	right_text.draw()
	gabor_right_example_vis.draw()
	win.flip()
	event.waitKeys(keyList='space')
	instructions_text5.draw()
	instructions_text6.draw()
	win.flip()
	event.waitKeys(keyList='space')
	example_text.draw()
	win.flip()
	event.waitKeys(keyList='space')
	n_example.draw()
	gabor_left_example.draw()
	press_left_text.draw()
	win.flip()
	event.waitKeys(keyList=response_keys['left'])

	for i in range(80):
		fixation.draw()
		win.flip()


	#right


	n_example.draw()
	gabor_right_example.draw()
	press_right_text.draw()
	win.flip()
	event.waitKeys(keyList=response_keys['right'])
	instructions2_text.draw()
	win.flip()
	event.waitKeys(keyList='space')
	get_ready_text.draw()


### Main Experiment ###servicde
#clock reset
win.flip()


#trigger scanner
if scanner:
	#port.write(chr(np.uint8(128+32+64+1)))
    event.waitKeys(keyList=['t'])

experiment_clock.reset()

opacity = 0 # Initial Value for Opacity in Gabor, has to change
block_time = 0
for block in range(nr_blocks):
    if block_order[block] == 'gabor':
        opacity = gabor_opacity
    elif block_order[block] == 'control':
        opacity = control_opacity
    #Create Durations of 6 trials per block from gamma distribution
    min_gam = 2.65;
    max_gam = 3.65;
    hypothesized_blockdur = 6*3;

    sumBlockTiming = 1;
    currentBlockTrialTimes = 0 * nr_trial_per_block
    while not(sumBlockTiming > hypothesized_blockdur - 0.005) & (sumBlockTiming < hypothesized_blockdur):
        currGamRandSampleVect = np.random.gamma(3,1,10000)
        currGamRandSampleVect = currGamRandSampleVect[(currGamRandSampleVect > min_gam) & (currGamRandSampleVect < max_gam)]
        currentBlockTrialTimes = rd.choices(currGamRandSampleVect, k = nr_trial_per_block)
        sumCurrentBlockTrialTimes = sum(currentBlockTrialTimes)
        if sumCurrentBlockTrialTimes < hypothesized_blockdur:
            sumBlockTiming = sumCurrentBlockTrialTimes

    #Create the angle of the trials and shuffle them
    trial_states = {}
    n = 0
    elapse_time = block_time
    last_trial_dur = 0
    for i in range(int(nr_trial_per_block)):
        n+=1
        trial_states[n] = {'target':'left'}
        n+=1
        trial_states[n] = {'target':'right'}
    trial_order = list(range(1,(1+nr_trial_per_block)))
    rd.shuffle(trial_order)

    trial = 0

    for shuffled_trial in trial_order:
        trial += 1
        target_side = trial_states[shuffled_trial]['target']
        if (target_side == 'left'):
            side = 'left'
            gabor_tex = (
            visual.filters.makeGrating(res=X, cycles=X * sf, ori = left, gratType = "sin" ) *
            visual.filters.makeMask(matrixSize=X, shape="gauss", range=[0, 1])
            )
        else:
            side = 'right'
            gabor_tex = (
            visual.filters.makeGrating(res=X, cycles=X * sf, ori = right, gratType = "sin" ) *
            visual.filters.makeMask(matrixSize=X, shape="gauss", range=[0, 1])
            )

        elapse_time += last_trial_dur
        stim_onset = elapse_time
        response_end = elapse_time + stim_dur
        trial_end = stim_onset + currentBlockTrialTimes[trial-1]

		# signal grating patch
        gabor = visual.GratingStim(win = win, tex = gabor_tex, mask = None, units = 'pix',  size = X, contrast = 1.0, opacity = opacity)

        #stim presentation
        responded = False
        response = []
        event.clearEvents(eventType=None)
		port.setData(0)
		if block == 'control':
			win.callOnFlip(port.setData, 9)
		else:
			win.callOnFlip(port.setData, 18)
        while experiment_clock.getTime() < response_end:
            noise.draw()
            gabor.draw()
            fixation.draw()
            if responded:
                fixation_green.draw()
            win.flip()
		#event.waitKeys(keyList=reskeys_list)
		#response collection
            if not responded:
                response = event.getKeys(keyList=reskeys_list, timeStamped=True)
                if len(response) > 0:
                    responded = True
                    cumulative_response_time = round(experiment_clock.getTime(),3)
                    response_time = round(experiment_clock.getTime() - elapse_time,3)
                    sub_response = response_keys_inv[response[0][0]]
                    if sub_response == side:
                        correct = 1
                    else:
                        correct = 0
                    output_file.write(','.join([str(trial),str(side),str(sub_response),str(correct),str(response_time),str(cumulative_response_time),str(currentBlockTrialTimes[trial-1]),str(stim_onset),str(stim_dur),str(opacity)+'\n']))
                    output_file.flush()
		win.callOnFlip(port.setData, 0)
        if not responded:
            correct = 0
            fixation.draw()
            output_file.write(','.join([str(trial),str(side),'NA',str(correct),'NA','NA',str(currentBlockTrialTimes[trial-1]),str(stim_onset),str(stim_dur),str(opacity)+'\n']))
            output_file.flush()
            win.flip()
        while experiment_clock.getTime() < trial_end:
            fixation.draw()
            win.flip()
        #timing update
        last_trial_dur = currentBlockTrialTimes[trial-1]
        block_time = elapse_time + last_trial_dur

    while experiment_clock.getTime() < block_time + duration_rest:
        fixation.draw()
        win.flip()

    block_time = block_time + duration_rest



output_file.close()
win.close()
