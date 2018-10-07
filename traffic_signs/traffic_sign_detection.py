#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Usage:
  traffic_sign_detection.py <outPath>
  traffic_sign_detection.py -h | --help
Options:
  --windowMethod=<wm>        Window method       [default: 'None']
"""


from docopt import docopt
import numpy as np
import fnmatch
import os
import imageio
from candidate_generation_pixel import candidate_generation_pixel

def traffic_sign_detection(directory, output_dir, pixel_methods, window_method):

    # Load image names in the given directory
    file_names = sorted(fnmatch.filter(os.listdir(directory), '*.jpg'))

    for method in pixel_methods:
        for name in file_names:
            base, extension = os.path.splitext(name)

            # Read file
            im = imageio.imread('{}/{}'.format(directory,name))
            print ('{}/{}'.format(directory,name))

            # Candidate Generation (pixel) ######################################
            pixel_candidates = candidate_generation_pixel(im, method)

            fd = '{}/{}_{}'.format(output_dir, method, window_method)
            if not os.path.exists(fd):
                os.makedirs(fd)

            out_mask_name = '{}/mask.{}.png'.format(fd, base)
            imageio.imwrite(out_mask_name, np.uint8(np.round(pixel_candidates)))

                
if __name__ == '__main__':
    # read arguments
    args = docopt(__doc__)

    images_dir = './test'          # Directory with input images and annotations
                                            # For instance, '../../DataSetDelivered/test'
    output_dir = args['<outPath>']          # Directory where to store output masks, etc. For instance '~/m1-results/week1/test'

    methodMask = ['rgb','YCbCr','hsv']

    traffic_sign_detection(images_dir, output_dir, methodMask, 'None')


    
