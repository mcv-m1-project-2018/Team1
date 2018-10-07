#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Usage:
  database_analysis_main.py <dirName>
  database_analysis_main.py -h | --help
"""
from docopt import docopt
import numpy as np
import fnmatch
import imageio
import os
import database_analysis.analysis_utils as imutil
import matplotlib.pyplot as plt
import cv2
from sklearn.mixture import GaussianMixture

import sys
import math




def main(directory):
    evaluate_elements = ['gt', 'mask']
    dirname = '{}/..{}'.format(os.path.dirname(__file__), directory)
    file_names = sorted(fnmatch.filter(os.listdir(dirname), '*.jpg'))
    database_info = dict()
    database_info["image"] = list()
    database_info["type"] = list()
    database_info["height_box"] = list()
    database_info["width_box"] = list()
    database_info["form_factor"] = list()
    database_info["filling_ratio"] = list()
    database_info["mask_area"] = list()
    database_info["background_area"] = list()
    database_info["frecuency_typeA"] = 0
    database_info["frecuency_typeB"] = 0
    database_info["frecuency_typeC"] = 0
    database_info["frecuency_typeD"] = 0
    database_info["frecuency_typeE"] = 0
    database_info["frecuency_typeF"] = 0
    database_info["r_channel_hist"] = list()
    database_info["g_channel_hist"] = list()
    database_info["b_channel_hist"] = list()

    count_frecunacy_typeA = 0
    count_frecunacy_typeB = 0
    count_frecunacy_typeC = 0
    count_frecunacy_typeD = 0
    count_frecunacy_typeE = 0
    count_frecunacy_typeF = 0

    count_img = 0

    image_types = ['A', 'B', 'C', 'D', 'E', 'F']

    for name in file_names:
        count_img = count_img + 1
        name_gt = 'gt.{}'.format(name.replace('.jpg', '.txt'))
        name_mask = 'mask.{}'.format(name.replace('.jpg', '.png'))

        path_image = '{}/{}'.format(dirname, name)
        path_image_gt = '{}/{}/{}'.format(dirname, evaluate_elements[0], name_gt)
        path_image_mask = '{}/{}/{}'.format(dirname, evaluate_elements[1], name_mask)

        im_current = imageio.imread(path_image)
        im_current_mask = imageio.imread(path_image_mask)

        # imutil.visualize_image(im_current)
        database_info["image"].append(name)

        # Read .txt info
        with open(path_image_gt) as f:
            lines = f.readlines()

            topy, topx, downy, downx, types = lines[0].split(' ')

            types = '{}'.format(types).rstrip()
            database_info["type"].append(types)

            if types == 'A':
                count_frecunacy_typeA = count_frecunacy_typeA + 1
            elif types == 'B':
                count_frecunacy_typeB = count_frecunacy_typeB + 1
            elif types == 'C':
                count_frecunacy_typeC = count_frecunacy_typeC + 1
            elif types == 'D':
                count_frecunacy_typeD = count_frecunacy_typeD + 1
            elif types == 'E':
                count_frecunacy_typeE = count_frecunacy_typeE + 1
            elif types == 'F':
                count_frecunacy_typeF = count_frecunacy_typeF + 1

            aux_height = float(downx) - float(topx)
            aux_width = float(downy) - float(topy)

            database_info["height_box"].append(aux_height)
            database_info["width_box"].append(aux_width)
            database_info["form_factor"].append(aux_width / aux_height)

            topy_trunc = topy[:topy.index('.')]
            topx_trunc = topx[:topx.index('.')]
            downy_trunc = downy[:downy.index('.')]
            downx_trunc = downx[:downx.index('.')]
            crop_img = im_current_mask[int(topy_trunc):int(downy_trunc), int(topx_trunc):int(downx_trunc)]

            # imutil.visualize_image(crop_img)

            count_background = 0
            count_sig = 0
            for line in crop_img:
                for pixel in line:
                    if pixel == 1:
                        count_sig = count_sig + 1
                    else:
                        count_background = count_background + 1

            database_info["mask_area"].append(count_sig)
            database_info["background_area"].append(count_background)

            if (count_background == 0):
                database_info["filling_ratio"].append(1)
            else:
                database_info["filling_ratio"].append(count_sig / count_background)

    database_info["frecuency_typeA"] = count_frecunacy_typeA / count_img
    database_info["frecuency_typeB"] = count_frecunacy_typeB / count_img
    database_info["frecuency_typeC"] = count_frecunacy_typeC / count_img
    database_info["frecuency_typeD"] = count_frecunacy_typeD / count_img
    database_info["frecuency_typeE"] = count_frecunacy_typeE / count_img
    database_info["frecuency_typeF"] = count_frecunacy_typeF / count_img

    #imutil.create_table(
    #    ['image', 'Type', 'height_box', 'width_box', 'form_factor', 'filling_ratio', 'mask_area', 'background_area'],
    #    [database_info["image"], database_info["type"], database_info["height_box"], database_info["width_box"],
    #     database_info["form_factor"], database_info["filling_ratio"], database_info["mask_area"],
    #     database_info["background_area"]])

    images_by_type = dict()

    for type in image_types:
        index_of_type = imutil.divide_by_type(database_info["type"],type)
        list_images = list()
        for index in index_of_type:
            list_images.append(database_info["image"][index])
        images_by_type[type] = list_images.copy()
        list_images.clear()




    for i in images_by_type:

        final_his_f = 0
        initial_his_f = 0
        initial_his_f_hsv = 0
        final_his_f_hsv = 0

        bins_f = 0
        bins_f_hsv = 0

        for j in images_by_type[i]:
            im_current = imageio.imread('{}/{}'.format(dirname,j))
            path_image_gt = '{}/{}/{}'.format(dirname, evaluate_elements[0], 'gt.{}'.format(j.replace('.jpg', '.txt')))
            acumulate_hist_ch1 = np.zeros(255)
            acumulate_hist_ch2 = np.zeros(255)
            acumulate_hist_ch3 = np.zeros(255)
            acumulate_hist_ch1_hsv = np.zeros(255)
            acumulate_hist_ch2_hsv = np.zeros(255)
            acumulate_hist_ch3_hsv = np.zeros(255)

            acumulate_im = np.array([])

            with open(path_image_gt) as f:
                lines = f.readlines()

                topy, topx, downy, downx, types = lines[0].split(' ')

                topy_trunc = topy[:topy.index('.')]
                topx_trunc = topx[:topx.index('.')]
                downy_trunc = downy[:downy.index('.')]
                downx_trunc = downx[:downx.index('.')]
                crop_img_signal = im_current[int(topy_trunc):int(downy_trunc), int(topx_trunc):int(downx_trunc)]
                if(acumulate_im.size == 0):
                    acumulate_im = crop_img_signal
                acumulate_im += crop_img_signal

                bins, his_ch1, init_his, final_his = imutil.acumulate_hist(crop_img_signal,'RGB','ch1')
                bins, his_ch2, init_his, final_his = imutil.acumulate_hist(crop_img_signal, 'RGB', 'ch2')
                bins, his_ch3, init_his, final_his = imutil.acumulate_hist(crop_img_signal, 'RGB', 'ch3')
                acumulate_hist_ch1 += his_ch1
                acumulate_hist_ch2 += his_ch2
                acumulate_hist_ch3 += his_ch3

                bins_hsv, his_ch1_hsv, init_his_hsv, final_his_hsv = imutil.acumulate_hist(crop_img_signal, 'HSV', 'ch1')
                bins_hsv, his_ch2_hsv, init_his_hsv, final_his_hsv = imutil.acumulate_hist(crop_img_signal, 'HSV', 'ch2')
                bins_hsv, his_ch3_hsv, init_his_hsv, final_his_hsv = imutil.acumulate_hist(crop_img_signal, 'HSV', 'ch3')
                acumulate_hist_ch1_hsv += his_ch1_hsv
                acumulate_hist_ch2_hsv += his_ch2_hsv
                acumulate_hist_ch3_hsv += his_ch3_hsv

                initial_his_f = init_his
                final_his_f = final_his

                initial_his_f_hsv= init_his_hsv
                final_his_f_hsv = final_his_hsv


        gmm = acumulate_im.ravel() / np.size(images_by_type[i])
        imutil.visualize_histogram('histogram signal type {}'.format(i),acumulate_hist_ch1, acumulate_hist_ch2, acumulate_hist_ch3,initial_his_f, final_his_f, gmm)

        imutil.visualize_histogram('histogram signal type {}'.format(i),acumulate_hist_ch1_hsv, acumulate_hist_ch2_hsv, acumulate_hist_ch3_hsv,initial_his_f_hsv, final_his_f_hsv, gmm)



if __name__ == "__main__":
    # read arguments
    args = docopt(__doc__)

    images_dir = args['<dirName>']  # Directory with input images and annotations

    main(images_dir)
