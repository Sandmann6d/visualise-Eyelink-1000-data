# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 16:22:32 2021

@author: Viktor
"""


import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


csv_file = 'fixations_report.csv'
# Eyetracking data converted to .csv. It should include the columns
# 'RECORDING_SESSION_LABEL', 'TRIAL_INDEX', 'VIDEO_FRAME_INDEX_START',
# 'CURRENT_FIX_X', 'CURRENT_FIX_Y', 'CURRENT_FIX_DURATION'.
# Make sure decimal points are '.' and not ','.
# In 'VIDEO_FRAME_INDEX_START', replace first frame marker with '1'.


all_sessions = ['VPN001', 'VPN002', 'VPN003', 'VPN004', 'VPN005', 'VPN006', \
                'VPN007', 'VPN008', 'VPN009', 'VPN010', 'VPN011']
# List of sessions / names of participants (str).     
    
session = 'VPN009'
trial = 8
first_frame = 1
last_frame = 180
pivot_frame = 90
# These can be entered directly into the functions.

x_axis = 1920
y_axis = 1080
# Resolution of eye tracker.

image = 'trial06_2.jpeg'
plot_over_image = True
# Choose image from working directory to plot over. Or plot over blank space.

save_plotted_image = True
dpi = 200

def load_image(image):
    '''Loads an image to plot over.
    Args:
        image(string): name of the image file in working directory, read
                       from variable 'image'.
    '''
    img = mpimg.imread(image)
    fig, ax = plt.subplots()
    ax.imshow(img, extent=[0, x_axis, y_axis, 0])

def save_or_show(session, trial, first_frame, last_frame):
    '''Shows the plotted image under plots. 
    Optional: Save plotted image in working directory.
    Args:
        session (str): name of session or participant.
        trial (int): number of trial.
        first_frame (int): fixations starting at or after this video frame 
                           will be plotted (min. 1).
        last_frame (int): fixations starting at or before this video frame
                          will be plotted. Must be larger than first_frame.
    Returns:
        plot, and optionally saves image file under filename format.
    '''
    if save_plotted_image:
        filename = session + '_trial' + str(trial) + '_' + \
                   str(first_frame) + '_' + str(last_frame)
        plt.savefig(filename, dpi=dpi)
    else:
        plt.show()

def plot_simple(session, trial, first_frame, last_frame): 
    '''Plots fixations as circles (the longer the fixation, the larger the
    circle), numbers them and draws lines between the centre points.
    Args:
        session (str): name of session or participant.
        trial (int): number of trial.
        first_frame (int): fixations starting at or after this video frame 
                           will be plotted (min. 1).
        last_frame (int): fixations starting at or before this video frame
                          will be plotted. Must be larger than first_frame.
    Returns:
        plot.
    '''
    x, y, duration = [], [], []
    
    if plot_over_image:
        load_image(image)
        
    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            session_trial_check = row['RECORDING_SESSION_LABEL'] == session \
            and int(row['TRIAL_INDEX']) == trial
            if session_trial_check and first_frame <= \
            float(row['VIDEO_FRAME_INDEX_START']) <= last_frame:
                x.append(float(row['CURRENT_FIX_X']))
                y.append(float(row['CURRENT_FIX_Y']))
                duration.append(float(row['CURRENT_FIX_DURATION']))
            
    plt.plot(x, y, 'xkcd:orange')
    plt.scatter(x, y, duration, 'xkcd:baby blue')
    plt.axis([0, x_axis, y_axis, 0])
    ax = plt.gca()
    ax.axes.xaxis.set_ticks([])
    ax.axes.yaxis.set_ticks([])
    
    i = 1
    for x,y in zip(x,y):
        plt.annotate(str(i),(x,y), ha='center') 
        i += 1
        
    save_or_show(session, trial, first_frame, last_frame)



def plot_pivot(session, trial, first_frame, last_frame, pivot_frame): 
    '''Plots fixations as circles (the longer the fixation, the larger the
    circle), numbers them and draws lines between the centre points. Fixations
    before, at, and after a designated video frame are coloured differently.
    Args:
        session (str): name of session or participant.
        trial (int): number of trial.
        first_frame (int): fixations starting at or after this video frame 
                           will be plotted (min. 1).
        last_frame (int): fixations starting at or before this video frame
                          will be plotted. Must be larger than first_frame.
        pivot_frame (int): the fixation starting right before this video frame
                           changes colour. Between first_frame and last_frame.
    Returns:
        plot.
    '''
    x1, y1, duration1 = [], [], []
    x2, y2, duration2 = [], [], []
    
    if plot_over_image:
        load_image(image)
    
    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            session_trial_check = row['RECORDING_SESSION_LABEL'] == session \
            and int(row['TRIAL_INDEX']) == trial
            if session_trial_check and pivot_frame <= \
            float(row['VIDEO_FRAME_INDEX_START']) <= last_frame:
                x2.append(float(row['CURRENT_FIX_X']))
                y2.append(float(row['CURRENT_FIX_Y']))
                duration2.append(float(row['CURRENT_FIX_DURATION']))
            elif session_trial_check and first_frame <= \
            float(row['VIDEO_FRAME_INDEX_START']) <= pivot_frame:
                x1.append(float(row['CURRENT_FIX_X']))
                y1.append(float(row['CURRENT_FIX_Y']))
                duration1.append(float(row['CURRENT_FIX_DURATION']))
    
    x_concat = np.concatenate((x1, x2))
    y_concat = np.concatenate((y1, y2))          
    
    plt.plot(x_concat, y_concat, 'xkcd:orange')
    plt.scatter(x1, y1, duration1, 'xkcd:green')
    plt.scatter(x2[0], y2[0], duration2[0], 'xkcd:yellow green')
    plt.scatter(x2[1:], y2[1:], duration2[1:], 'xkcd:yellow')
    plt.axis([0, x_axis, y_axis, 0])
    ax = plt.gca()
    ax.axes.xaxis.set_ticks([])
    ax.axes.yaxis.set_ticks([])
    
    i = 1
    for x_concat, y_concat in zip(x_concat,y_concat):
        plt.annotate(str(i),(x_concat,y_concat), ha='center') 
        i += 1
    
    save_or_show(session, trial, first_frame, last_frame)
    


def plot_pivot2(session, trial, first_frame, last_frame, pivot_frame, pivot_frame2):
    '''Plots fixations as circles (the longer the fixation, the larger the
    circle), numbers them and draws lines between the centre points. Fixations
    before, at, and after two designated video frames are coloured differently.
    Args:
        session (str): name of session or participant.
        trial (int): number of trial.
        first_frame (int): fixations starting at or after this video frame 
                           will be plotted (min. 1).
        last_frame (int): fixations starting at or before this video frame
                          will be plotted. Must be larger than first_frame.
        pivot_frame (int): the fixation starting right before this video frame
                           changes colour. Between first_frame and pivot_frame2.
        pivot_frame2 (int): the fixation starting right before this video frame
                            changes colour once more. Between pivot_frame and last_frame.
    Returns:
        plot.
    '''
    x1, y1, duration1 = [], [], []
    x2, y2, duration2 = [], [], []
    x3, y3, duration3 = [], [], []
    
    if plot_over_image:
        load_image(image)
    
    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            session_trial_check = row['RECORDING_SESSION_LABEL'] == session \
            and int(row['TRIAL_INDEX']) == trial
            if session_trial_check and pivot_frame2 <= \
            float(row['VIDEO_FRAME_INDEX_START']) <= last_frame:
                x3.append(float(row['CURRENT_FIX_X']))
                y3.append(float(row['CURRENT_FIX_Y']))
                duration3.append(float(row['CURRENT_FIX_DURATION']))
            elif session_trial_check and pivot_frame <= \
            float(row['VIDEO_FRAME_INDEX_START']) <= pivot_frame2:
                x2.append(float(row['CURRENT_FIX_X']))
                y2.append(float(row['CURRENT_FIX_Y']))
                duration2.append(float(row['CURRENT_FIX_DURATION']))
            elif session_trial_check and first_frame <= \
            float(row['VIDEO_FRAME_INDEX_START']) <= pivot_frame:
                x1.append(float(row['CURRENT_FIX_X']))
                y1.append(float(row['CURRENT_FIX_Y']))
                duration1.append(float(row['CURRENT_FIX_DURATION']))
    
    x_concat = np.concatenate((x1, x2, x3))
    y_concat = np.concatenate((y1, y2, y3))          
    
    plt.plot(x_concat, y_concat, 'xkcd:orange')
    plt.scatter(x1, y1, duration1, 'xkcd:baby blue')
    plt.scatter(x2[0], y2[0], duration2[0], 'xkcd:sea green')
    plt.scatter(x2[1:], y2[1:], duration2[1:], 'xkcd:green')
    plt.scatter(x3[0], y3[0], duration3[0], 'xkcd:yellow green')
    plt.scatter(x3[1:], y3[1:], duration3[1:], 'xkcd:yellow')
    plt.axis([0, x_axis, y_axis, 0])
    ax = plt.gca()
    ax.axes.xaxis.set_ticks([])
    ax.axes.yaxis.set_ticks([])
    
    i = 1
    for x_concat, y_concat in zip(x_concat,y_concat):
        plt.annotate(str(i),(x_concat,y_concat), ha='center') 
        i += 1
        
    save_or_show(session, trial, first_frame, last_frame)
    


def all_sessions_to_images(pivots, trial, first_frame, last_frame, \
                           pivot_frame=None, pivot_frame2=None):
    '''Calls one of the plotting functions and applies them to all sessions / 
    participants. Saves all plots as image files in working directory.
    Args:
        pivots (0, 1, or 2): number of pivot frames.
        trial (int): number of trial.
        first_frame (int): fixations starting at or after this video frame 
                           will be plotted (min. 1).
        last_frame (int): fixations starting at or before this video frame
                          will be plotted. Must be larger than first_frame.
        pivot_frame (int): optional, if pivots is 1 or 2. The fixation starting 
                           right before this video frame changes colour. 
                           Between first_frame and last_frame.
        pivot_frame2 (int): optional, if pivots is 2. The fixation starting 
                            right before this video frame changes colour once 
                            more. Between pivot_frame and last_frame.
    Returns:
        plot and image file.
    '''
    i = 0
    while i < len(all_sessions):
        session = all_sessions[i]
        global save_plotted_image        
        save_plotted_image = True
        if pivots == 0:
            plot_simple(session, trial, first_frame, last_frame)
            plt.close()
        elif pivots == 1:
            plot_pivot(session, trial, first_frame, last_frame, pivot_frame)
            plt.close()
        elif pivots == 2:
            plot_pivot2(session, trial, first_frame, last_frame, pivot_frame, pivot_frame2)
            plt.close()
        i += 1

#plot_pivot(session, trial, first_frame, last_frame, pivot_frame)
#plot_pivot('VPN005', 8, 1, 150, 18)
all_sessions_to_images(1, 6, 634, 754, 694)
#plot_simple('VPN001', 1, 1, 150)  
#plot_pivot2('VPN011', 8, 136, 285, 196, 225)   
#plot_simple('VPN010', 8, 136, 285) 