import database_analysis.analysis_utils as imutil
import random
import numpy as np

'''
Spliting the training data in two parts 70%/30%.
The first part is for training and the second for 
validation.
'''

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
        validationData[type] = np.setdiff1d(images_by_type[type], trainingData[type]).tolist()

    return trainingData, validationData