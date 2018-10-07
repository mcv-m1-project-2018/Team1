#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from skimage import color
import matplotlib as plt
import matplotlib.pyplot as plt

def candidate_generation_pixel_hsv(im):

    hsv_im = color.rgb2hsv(im)

    mask_red = (((hsv_im[:,:,0] < 0.03) | (hsv_im[:,:,0] > 0.9)))
    mask_blue = ((hsv_im[:,:,0] > 0.55) & (hsv_im[:,:,0] < 0.75))

    final_mask =mask_red + mask_blue

    return final_mask

def canditate_generation_pixel_histogram_equalization(im):

    hist, bins = np.histogram(im.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * hist.max() / cdf.max()
    plt.plot(cdf_normalized, color='b')
    plt.hist(im.flatten(), 256, [0, 256], color='r')
    plt.xlim([0, 256])
    plt.legend(('cdf', 'histogram'), loc='upper left')
    plt.show()

    return 0

def candidate_generation_pixel_YCbCr(im):

    imYCbCr = color.rgb2ycbcr(im)
    hsv_im = color.rgb2hsv(im)

    mask_Cr_RR = ((imYCbCr[:,:,2] > 140) & (imYCbCr[:,:, 2] < 190))

    mask_blue = ((hsv_im[:, :, 0] > 0.55) & (hsv_im[:, :, 0] < 0.75))

    finalMask = mask_Cr_RR + mask_blue

    return finalMask

def candidate_generation_pixel_RGB(im):
    mask_channel_red = ((im[:, :, 0] > 70) & (im[:, :, 1] < 55)& (im[:, :, 2] < 55))
    mask_channel_blue = ((im[:, :, 0] <50) & (im[:, :, 1] < 90)& (im[:, :, 2] > 55))

    final_mask = mask_channel_red + mask_channel_blue

    return final_mask
 
# Create your own candidate_generation_pixel_xxx functions for other color spaces/methods
# Add them to the switcher dictionary in the switch_color_space() function
# These functions should take an image as input and output the pixel_candidates mask image
 
def switch_color_space(im, color_space):
    switcher = {
        'YCbCr': candidate_generation_pixel_YCbCr,
        'hsv': candidate_generation_pixel_hsv,
        'eq_histogram': canditate_generation_pixel_histogram_equalization,
        'rgb':candidate_generation_pixel_RGB
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

    
