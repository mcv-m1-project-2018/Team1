#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import time
import cv2
import database_analysis.analysis_utils as imutil

'''
Tools for detecting signals using a mask. A square 
will be drawn at every detected signal. The threshold 
of each signal class and each filling ratio are used 
to determine if we detect a signal on the image.  
'''

def candidate_generation_window_example1(im, pixel_candidates,thresholds):
    window_candidates = []

    (winW, winH) = (126, 126)

    # loop over the image pyramid
    for resized in pyramid(im, scale=1.5):
        # loop over the sliding window for each layer of the pyramid
        for (x, y, window) in sliding_window(resized, stepSize=32, windowSize=(winW, winH)):
            # if the window does not meet our desired window size, ignore it
            if window.shape[0] != winH or window.shape[1] != winW:
                continue
            crop_img = pixel_candidates[int(y):int(y + winH), int(x):int(x + winW)]

            area_signal, area_background = info_image_segment(crop_img)
            if(area_background==0):
                filling_ratio = 1
            else:
                filling_ratio = area_signal / area_background
            is_signal, type_signal=is_windows_signal(filling_ratio,thresholds)
            #imutil.visualize_image(crop_img)
            if is_signal:
                window_candidates.append([y,y + winH, x,x + winW])
                #imutil.visualize_image(crop_img)

            # THIS IS WHERE YOU WOULD PROCESS YOUR WINDOW, SUCH AS APPLYING A
            # MACHINE LEARNING CLASSIFIER TO CLASSIFY THE CONTENTS OF THE
            # WINDOW

            # since we do not have a classifier, we'll just draw the window
            clone = resized.copy()
            #cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
            #cv2.imshow("Window", clone)
            #cv2.waitKey(1)
    return window_candidates
 
def candidate_generation_window_example2(im, pixel_candidates,thresholds):
    window_candidates = [[21.0, 14.0, 54.0, 47.0], [63.0,92.0,103.0,132.0],[200.0,200.0,250.0,250.0]]
    # sfdfwer

    return window_candidates

def info_image_segment(im):
    count_background = 0
    count_sig = 0
    for line in im:
         for pixel in line:
            if pixel == 1:
             count_sig = count_sig + 1
            else:
             count_background = count_background + 1

    return count_sig, count_background

# Create your own candidate_generation_window_xxx functions for other methods
# Add them to the switcher dictionary in the switch_method() function
# These functions should take an image, a pixel_candidates mask (and perhaps other parameters) as input and output the window_candidates list.
def sliding_window(image, stepSize, windowSize):
    # slide a window across the image
    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            # yield the current window
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])

def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized

def pyramid(image, scale=1.5, minSize=(30, 30)):
    # yield the original image
    yield image

    # keep looping over the pyramid
    while True:
        # compute the new dimensions of the image and resize it
        w = int(image.shape[1] / scale)
        image = resize(image, width=w)

        # if the resized image does not meet the supplied minimum
        # size, then stop constructing the pyramid
        if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
            break

        # yield the next image in the pyramid
        yield image
def is_windows_signal(current_ratio,ratios):

    id_signal = False
    type_signal =''
    if ratios['A'][0]< current_ratio<ratios['A'][1]:
        id_signal = True
        type_signal ='A'
    elif ratios['B'][0]< current_ratio<ratios['B'][1]:
        id_signal = True
        type_signal = 'B'
    elif ratios['C'][0]< current_ratio<ratios['C'][1]:
        id_signal = True
        type_signal = 'C'
    elif ratios['D'][0]< current_ratio<ratios['D'][1]:
        id_signal = True
        type_signal = 'D'
    elif ratios['E'][0]< current_ratio<ratios['E'][1]:
        id_signal = True
        type_signal = 'E'
    elif ratios['F'][0]< current_ratio<ratios['F'][1]:
        id_signal = True
        type_signal = 'F'

    return id_signal,type_signal

def switch_method(im, pixel_candidates, method,thresholds):
    switcher = {
        'example1': candidate_generation_window_example1,
        'example2': candidate_generation_window_example2
    }
    # Get the function from switcher dictionary
    func = switcher.get(method, lambda: "Invalid method")

    # Execute the function
    window_candidates = func(im, pixel_candidates,thresholds)

    return window_candidates

def candidate_generation_window(im, pixel_candidates, method, thresholds):

    window_candidates = switch_method(im, pixel_candidates, method, thresholds)

    return window_candidates



    
