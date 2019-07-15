#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from psychopy import  gui, visual, core, data, event, logging
from time import strftime
import pandas as pd
from random import choice
from numpy.random import choice as choice2
import numpy as np
import random
import csv
import pandas
import matplotlib
import matplotlib.pyplot as plt
from psychopy.tools.filetools import fromFile
import pylab
import os
from operator import truediv

#Open Dialog for file
files = gui.fileOpenDlg('./results/')
file = files[0]


full_filename = os.path.splitext(os.path.basename(file))
filename = full_filename[0]

save_dir = os.path.dirname(file)

## Plot the staircase data to get the threshold
matplotlib.style.use('ggplot')
plt.style.use('seaborn-dark-palette')
colors = {0:'red', 1:'green'}
data = pandas.read_csv(file)
data['corr_factor'] = data['correct'].astype('category')
data['rounded_opacity'] = round(data['opacity'],5)

data['shifted_direction'] = data['currentDirection'].shift(-1)
data['reversalPoint'] = data.shifted_direction.eq(data.shifted_direction.shift())
new_data = data.drop([data.index[0],data.index[-1]])
threshold = round(new_data[new_data['reversalPoint'] == False]['opacity'].mean(),4)
print(threshold)
#Plot1

w = 8
h = 6
d = 96
plt.figure(figsize= (w,h), dpi = d)
plt.plot(data['trial'], data['opacity'])
plt.scatter(data = data, x='trial', y = 'opacity', c = data['corr_factor'].apply(lambda x: colors[x]), label = 'corr_factor', s = 1)
plt.title('Trial pathway')
plt.xlabel('Trial')
plt.ylabel('Opacity')

plt.savefig(save_dir+'/'+filename+'_trialPath.pdf')
plt.close()

#Plot2
opacities = np.unique(data['rounded_opacity'])
#cat_durations = ",".join(str(s) for s in durations)
#cat_durations = [ '%.2f' % elem for elem in durations]



nTrials = []
nCorrect = []
for i in range(len(opacities)):
    id = data['rounded_opacity'] == opacities[i]
    nTrials.append(sum(id*1))
    nCorrect.append(sum((data['correct'][id])))


pCorrect = np.divide(nCorrect,nTrials)


#dataframe for correctness, nTrials, etc

sumData = pd.DataFrame({'opacities': opacities.astype('str'),'pCorrect':pCorrect*100,'nTrials':nTrials})





plt.scatter(data = sumData, x = 'opacities', y = 'pCorrect', s = 'nTrials')

plt.title('Correct Responses by opacity level')
plt.xlabel('Opacity')
plt.ylabel('Percentage Correct')

plt.savefig(save_dir+'/'+filename+'_stimdur.pdf')

print('Done!')

core.quit()
