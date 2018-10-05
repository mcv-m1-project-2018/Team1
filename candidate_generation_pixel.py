#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from skimage import color
import matplotlib as plt
import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
#import cv2

def candidate_generation_pixel_normrgb(im):
    # convert input image to the normRGB color space

    normrgb_im = np.zeros(im.shape)
    eps_val = 0.00001
    norm_factor_matrix = im[:,:,0] + im[:,:,1] + im[:,:,2] + eps_val

    normrgb_im[:,:,0] = im[:,:,0] / norm_factor_matrix
    normrgb_im[:,:,1] = im[:,:,1] / norm_factor_matrix
    normrgb_im[:,:,2] = im[:,:,2] / norm_factor_matrix
    
    # Develop your method here:
    # Example:
    pixel_candidates = normrgb_im[:,:,1]>100 & normrgb_im[:,:,2]>100 & normrgb_im[:,:,3]>100;

    return pixel_candidates
 
def candidate_generation_pixel_hsv(im):
    # convert input image to HSV color space
    hsv_im = color.rgb2hsv(im)
    
    # Develop your method here:
    # Example:
    pixel_candidates = hsv_im[:,:,1] > 0.4;

    return pixel_candidates




def candidate_generation_pixel_histogram(im):
    # convert input image to HSV color space
    #hsv_im = color.rgb2hsv(im)

    plt.imshow(im)
    plt.show()

    imYCbCr = color.rgb2ycbcr(im)
    mask_Cr_RR = ((imYCbCr[:,:,2] > 140) & (imYCbCr[:,:, 2] < 190));
    #mask_Cr_BR = ((imYCbCr[:, :, 1] > 100) & (imYCbCr[:, :, 1] < 230));
    #mask_Cr_GR = ((imYCbCr[:, :, 0] > -40) & (imYCbCr[:, :, 0] < 66));

    finalMask = mask_Cr_RR

    #low = [0, 0, 30]
    #low = np.asarray(low)
    #hi = [60, 79, 196]
    #hi = np.asarray(hi)

    #finalMask = cv2.inRange(imYCbCr, low,hi)

    #plt.imshow(mask_Cr_RR)
    #plt.show()
    #plt.imshow(mask_Cr_BR)
    #plt.show()
    #plt.imshow(mask_Cr_GR)
    #plt.show()
    plt.imshow(finalMask)
    plt.show()

    imGreyScale =  np.sum(im.astype(np.int), axis=2) / 3

    # Develop your method here:
    # Example:

    return finalMask
 
# Create your own candidate_generation_pixel_xxx functions for other color spaces/methods
# Add them to the switcher dictionary in the switch_color_space() function
# These functions should take an image as input and output the pixel_candidates mask image
 
def switch_color_space(im, color_space):
    switcher = {
        'normrgb': candidate_generation_pixel_normrgb,
        'hsv'    : candidate_generation_pixel_hsv,
        'histogram' : candidate_generation_pixel_histogram,
        #'lab'    : candidate_generation_pixel_lab,
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

    
