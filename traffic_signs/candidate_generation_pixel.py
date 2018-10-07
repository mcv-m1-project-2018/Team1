#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from skimage import color
import matplotlib as plt
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
from sklearn.mixture import GaussianMixture
import database_analysis.analysis_utils as imutil
import pyramid
import argparse
import time

'''
Tools for generate a mask using the specified method YCbCr, hsv,
lab. Depending on the method selected, the mask will be on different
color spaces.
'''

def candidate_generation_pixel_hsv(im):

    hsv_im = color.rgb2hsv(im)

    #imutil.visualize_image(hsv_im)

    mask_red = (((hsv_im[:,:,0] < 0.03) | (hsv_im[:,:,0] > 0.9)))
    mask_blue = ((hsv_im[:,:,0] > 0.55) & (hsv_im[:,:,0] < 0.75))

    #imutil.visualize_image(mask_red)
    #imutil.visualize_image(mask_blue)

    final_mask =mask_red + mask_blue
    #imutil.visualize_image(final_mask)

    return final_mask

def canditate_generation_pixel_lab(im):

    return 0

def candidate_generation_pixel_YCbCr(im):
    # convert input image to HSV color space
    #hsv_im = color.rgb2hsv(im)

    plt.imshow(im)
    plt.show()

    imYCbCr = color.rgb2ycbcr(im)
    hsv_im = color.rgb2hsv(im)

    mask_Cr_RR = ((imYCbCr[:,:,2] > 140) & (imYCbCr[:,:, 2] < 190))

    mask_blue = ((hsv_im[:, :, 0] > 0.55) & (hsv_im[:, :, 0] < 0.75))

    #mask_Cr_BR = ((imYCbCr[:, :, 1] > 100) & (imYCbCr[:, :, 1] < 230));
    #mask_Cr_GR = ((imYCbCr[:, :, 0] > -40) & (imYCbCr[:, :, 0] < 66));

    finalMask = mask_Cr_RR + mask_blue

    #plt.imshow(mask_blue)
    #plt.show()
    #plt.imshow(mask_Cr_GR)
    #plt.show()
    #plt.imshow(finalMask)
    #plt.show()

    return  finalMask




    # Develop your method here:
    # Example:
    # loop through all detected objects
 
# Create your own candidate_generation_pixel_xxx functions for other color spaces/methods
# Add them to the switcher dictionary in the switch_color_space() function
# These functions should take an image as input and output the pixel_candidates mask image
 
def switch_color_space(im, color_space):
    switcher = {
        'YCbCr': candidate_generation_pixel_YCbCr,
        'hsv'    : candidate_generation_pixel_hsv,
        'lab'    : canditate_generation_pixel_lab,
    }
    # Get the function from switcher dictionary
    func = switcher.get(color_space, lambda: "Invalid color space")

    # Execute the function
    pixel_candidates =  func(im)

    return pixel_candidates


def candidate_generation_pixel(im, color_space):

    pixel_candidates = switch_color_space(im, color_space)

    return pixel_candidates

    
if __name__ == '__main__':
    pixel_candidates1 = candidate_generation_pixel(im, 'normrgb')
    pixel_candidates2 = candidate_generation_pixel(im, 'hsv')

    
