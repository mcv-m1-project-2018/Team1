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
import random
import sys
import math

def main(directory):
    evaluate_elements = ['gt','mask']
    dirname = '{}/..{}'.format(os.path.dirname(__file__),directory)
    file_names = sorted(fnmatch.filter(os.listdir(dirname), '*.jpg'))

    traningInfo = getTrainingInfo(evaluate_elements, dirname, file_names)

    splitData(traningInfo)

#Splits the data 70% training / 30% validation
def splitData(traningInfo):
    image_types = ['A', 'B', 'C', 'D', 'E', 'F']
    images_by_type = dict()

    for type in image_types:
        index_of_type = imutil.divide_by_type(traningInfo["type"], type)
        list_images = list()
        for index in index_of_type:
            list_images.append(traningInfo["image"][index])
        images_by_type[type] = list_images.copy()
        list_images.clear()

    #70% of the images are for training
    trainingElements = 0.7

    trainingData = dict()
    validationData = dict()

    #taking random training elements
    for type in image_types:
        trainingData[type] = random.sample(images_by_type[type], round(len(images_by_type[type]) * trainingElements))
        #taking the rest of elements
        validationData[type] = np.setdiff1d(images_by_type[type], trainingData[type])

    data = dict()
    data["trainingData"] = trainingData
    data["validationData"] = validationData
    return data

def getTrainingInfo(evaluate_elements, dirname, file_names):
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

    #imutil.create_table(['image','Type','height_box', 'width_box','form_factor', 'filling_ratio','mask_area','background_area'], [database_info["image"] ,database_info["type"],database_info["height_box"], database_info["width_box"],database_info["form_factor"],database_info["filling_ratio"], database_info["mask_area"],database_info["background_area"]])

    database_info['typeThresholds'] = getThresholds(database_info)

    return database_info

def getThresholds(database_info):
    count = 0
    vectorA = []
    vectorB = []
    vectorC = []
    vectorD = []
    vectorE = []
    vectorF = []

    for type in database_info["type"]:
        #Few samples has no mask
        if database_info["filling_ratio"][count] != 0:
            if type == 'A':
                vectorA.append(database_info["filling_ratio"][count])
            elif type == 'B':
                vectorB.append(database_info["filling_ratio"][count])
            elif type == 'C':
                vectorC.append(database_info["filling_ratio"][count])
            elif type == 'D':
                vectorD.append(database_info["filling_ratio"][count])
            elif type == 'E':
                vectorE.append(database_info["filling_ratio"][count])
            elif type == 'F':
                vectorF.append(database_info["filling_ratio"][count])
        count += 1

    thresholds = dict()
    thresholds["A"] = [min(vectorA), max(vectorA)]
    thresholds["B"] = [min(vectorB), max(vectorB)]
    thresholds["C"] = [min(vectorC), max(vectorC)]
    thresholds["D"] = [min(vectorD), max(vectorD)]
    thresholds["E"] = [min(vectorE), max(vectorE)]
    thresholds["F"] = [min(vectorF), max(vectorF)]
    return thresholds

if __name__ == "__main__":
    # read arguments
    #args = docopt(__doc__)

    images_dir = '/train'  # Directory with input images and annotations

    main(images_dir)

