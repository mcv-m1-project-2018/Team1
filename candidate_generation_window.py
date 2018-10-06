#!/usr/bin/python
# -*- coding: utf-8 -*-
import database_analysis.analysis_utils as imutil
import cv2

def candidate_generation_window_example1(im, pixel_candidates):
    window_candidates = [[17.0, 12.0, 49.0, 44.0], [60.0,90.0,100.0,130.0]]

    x = 0
    y = 0
    initialPointX = -1
    initialPointY = -1
    finalPointX = -1
    finalPointY = -1

    for yAxis in pixel_candidates:  # It goes through the pixels to determine the starting point.
        for pixel in yAxis:
            if pixel == 1:
                # first point and second init
                if initialPointX == -1:
                    initialPointX = x
                    initialPointY = y
                    finalPointX = x
                    finalPointY = y
                if y > finalPointY:
                    finalPointY = y
                if x > finalPointX:
                    finalPointX = x
            # second point (reverse axis for y)
            elif initialPointX != -1:
                #prevent out of bounds
                #finish of the shape
                maxRange = 10
                linesWithNoOnes = 0
                for ySearch in range(0, maxRange):
                    if len(pixel_candidates) > y + ySearch:
                        if 1 not in pixel_candidates[y + ySearch][x-10:x+10]:
                            linesWithNoOnes += 1
                    else:
                        linesWithNoOnes += 1
                    if y - ySearch > 0:
                        if 1 not in pixel_candidates[y - ySearch][x-10:x+10]:
                            linesWithNoOnes += 1
                    else:
                        linesWithNoOnes += 1

                #not found
                if linesWithNoOnes/2 == maxRange:
                    cv2.rectangle(im, (initialPointX, initialPointY), (finalPointX, finalPointY), (255, 255, 0), 2)
                    initialPointX = -1
                    initialPointY = -1
                    finalPointX = -1
                    finalPointY = -1
            x += 1
        #reset x every new line
        x = 0
        y += 1

    #imutil.visualize_image(pixel_candidates)
    imutil.visualize_image(im)

    return window_candidates
 
def candidate_generation_window_example2(im, pixel_candidates):
    window_candidates = [[21.0, 14.0, 54.0, 47.0], [63.0,92.0,103.0,132.0],[200.0,200.0,250.0,250.0]]

    return window_candidates
 
# Create your own candidate_generation_window_xxx functions for other methods
# Add them to the switcher dictionary in the switch_method() function
# These functions should take an image, a pixel_candidates mask (and perhaps other parameters) as input and output the window_candidates list.
 
def switch_method(im, pixel_candidates, method):
    switcher = {
        'example1': candidate_generation_window_example1,
        'example2': candidate_generation_window_example2
    }
    # Get the function from switcher dictionary
    func = switcher.get(method, lambda: "Invalid method")

    # Execute the function
    window_candidates = func(im, pixel_candidates)

    return window_candidates

def candidate_generation_window(im, pixel_candidates, method):

    window_candidates = switch_method(im, pixel_candidates, method)

    return window_candidates

    
