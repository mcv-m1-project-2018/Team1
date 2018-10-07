#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Usage:
  database_analysis_main.py <DirName>
  database_analysis_main.py -h | --help
"""

from docopt import docopt
import fnmatch
import os
import imageio
import database_analysis.analysis_utils as imutil

def show_image(directory, pixel_methods, window_method):

    # Load image names in the given directory
    file_names = sorted(fnmatch.filter(os.listdir(directory), '*.jpg'))

    for method in pixel_methods:
        for name in file_names:
            base, extension = os.path.splitext(name)

            fd = '{}/{}_{}'.format(directory, method, window_method)


            out_mask_name = '{}/mask.{}.png'.format(fd, base)
            # Read file
            im = imageio.imread(out_mask_name)
            imR = imageio.imread('{}/{}'.format(directory, name))
            imutil.visualize_image(im)
            imutil.visualize_image(imR)

if __name__ == '__main__':
    # read arguments
    args = docopt(__doc__)                        # Directory with input images and annotations
                                                  # For instance, '../../DataSetDelivered/test'
    dir =  args['<DirName>']                      # Directory where to store output masks, etc. For instance '~/m1-results/week1/test'

    methodMask = ['rgb','YCbCr','hsv']

    show_image(dir,methodMask, 'None')


