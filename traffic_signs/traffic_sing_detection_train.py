#!/usr/bin/python
# -*- coding: utf-8 -*-

from docopt import docopt
import numpy as np
import fnmatch
import os
import sys
import imageio
from candidate_generation_pixel import candidate_generation_pixel
from candidate_generation_window import candidate_generation_window
from evaluation.load_annotations import load_annotations
import evaluation.evaluation_funcs as evalf
import training_database as td
import database_analysis.analysis_utils as imutil
import cv2

def traffic_sign_detection_train(directory, output_dir, pixel_method, window_method):
    pixelTP = 0
    pixelFN = 0
    pixelFP = 0
    pixelTN = 0

    windowTP = 0
    windowFN = 0
    windowFP = 0

    window_precision = 0
    window_accuracy = 0

    # Load image names in the given directory
    evaluate_elements = ['gt', 'mask']

    database_info = imutil.get_database_info(directory, evaluate_elements, verbose_im =False, verbose_tab =False)

    training_data, validation_data = td.splitData(database_info)

    count = 0
    for type in training_data:
        for name in training_data[type]:

            base, extension = os.path.splitext(name)

            # Read file
            im = imageio.imread('.{}/{}'.format(directory, name))
            print('{}/{}'.format(directory, name))

            # Candidate Generation (pixel) ######################################
            pixel_candidates = candidate_generation_pixel(im, 'hsv')

            fd = '.{}/{}_{}'.format(output_dir, 'lab', window_method)
            if not os.path.exists(fd):
                os.makedirs(fd)

            out_mask_name = '{}/{}.png'.format(fd, base)
            imageio.imwrite(out_mask_name, np.uint8(np.round(pixel_candidates)))

            fill_ratios = imutil.getThresholds_filing_ratio(database_info)
            if window_method != 'None':
                window_candidates = candidate_generation_window(im, pixel_candidates, window_method,fill_ratios)
           # clone = im.copy()
           # for window in window_candidates:
           #     cv2.rectangle(im, (window[2], window[0]), (window[3], window[1]), (0, 255, 0), 2)
           # imutil.visualize_image(clone)
            #cv2.waitKey(1)

            # Accumulate pixel performance of the current image #################
            print('{}/{}.png'.format(fd, base))
            pixel_annotation = imageio.imread('{}/{}.png'.format(fd, base)) > 0

            [localPixelTP, localPixelFP, localPixelFN, localPixelTN] = evalf.performance_accumulation_pixel(
                pixel_candidates, pixel_annotation)
            pixelTP = pixelTP + localPixelTP
            pixelFP = pixelFP + localPixelFP
            pixelFN = pixelFN + localPixelFN
            pixelTN = pixelTN + localPixelTN

            [pixel_precision, pixel_accuracy, pixel_specificity, pixel_sensitivity] = evalf.performance_evaluation_pixel(
                pixelTP, pixelFP, pixelFN, pixelTN)

            if window_method != 'None':
                #Accumulate object performance of the current image ################
                window_annotationss = load_annotations('.{}/gt/gt.{}.txt'.format(directory, base))
                [localWindowTP, localWindowFN, localWindowFP] = evalf.performance_accumulation_window(window_candidates,
                                                                                                      window_annotationss)
                windowTP = windowTP + localWindowTP
                windowFN = windowFN + localWindowFN
                windowFP = windowFP + localWindowFP

              #  #Plot performance evaluation
            [window_precision, window_sensitivity, window_accuracy] = evalf.performance_evaluation_window(windowTP,
                                                                                                              windowFN,
                                                                                                              windowFP)
            print(window_precision)
            print(window_sensitivity)
            print(window_accuracy)

    #return [pixel_precision, pixel_accuracy, pixel_specificity, pixel_sensitivity, window_precision, window_accuracy]
    return 0

if __name__ == '__main__':
    # read arguments

    images_dir = '/train'                                  # Directory with input images and annotations
                                                            # For instance, '../../DataSetDelivered/test'
    output_dir = '/train/results'                          # Directory where to store output masks, etc. For instance '~/m1-results/week1/test'

    methodMask = ['m1','m2','m3']

    pixel_precision, pixel_accuracy, pixel_specificity, pixel_sensitivity, window_precision, window_accuracy = traffic_sign_detection_train(images_dir, output_dir, methodMask, 'example1');

    print(pixel_precision, pixel_accuracy, pixel_specificity, pixel_sensitivity, window_precision, window_accuracy)


