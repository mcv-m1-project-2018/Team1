import matplotlib.pyplot as plt
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import imageio
import os
from skimage import color
from sklearn.mixture import GaussianMixture
import fnmatch

def visualize_image(im):
    # Shows the image
    plt.imshow(im)
    plt.show()


def get_database_info(directory, evaluate_elements,verbose_im, verbose_tab):

    evaluate_elements = evaluate_elements
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

    for name in file_names:
        count_img = count_img + 1
        name_gt = 'gt.{}'.format(name.replace('.jpg', '.txt'))
        name_mask = 'mask.{}'.format(name.replace('.jpg', '.png'))

        path_image = '{}/{}'.format(dirname, name)
        path_image_gt = '{}/{}/{}'.format(dirname, evaluate_elements[0], name_gt)
        path_image_mask = '{}/{}/{}'.format(dirname, evaluate_elements[1], name_mask)

        im_current = imageio.imread(path_image)
        im_current_mask = imageio.imread(path_image_mask)

        if verbose_im:
            visualize_image(im_current)

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
            if verbose_im:
                visualize_image(crop_img)

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

    if verbose_tab:
        create_table(
            ['image', 'Type', 'height_box', 'width_box', 'form_factor', 'filling_ratio', 'mask_area', 'background_area'],
            [database_info["image"], database_info["type"], database_info["height_box"], database_info["width_box"],
             database_info["form_factor"], database_info["filling_ratio"], database_info["mask_area"],
             database_info["background_area"]])

    return database_info

def create_table(headers, cells):
    plotly.tools.set_credentials_file(username='dani118', api_key='yysQUJQqMosoO7QNcxTY')
    py.sign_in("dani118", "yysQUJQqMosoO7QNcxTY")

    trace = go.Table(
        header=dict(values=headers),
        cells=dict(values=cells))

    data = [trace]
    py.plot(data, filename='basic_table')

def divide_by_type(dic_images,type):
    count = 0
    listIndexs= []
    for i in dic_images:
        if(i==type):
            listIndexs.append(count)
        count = count + 1

    return listIndexs


def acumulate_hist(im, space,channel):
    init_his = 0
    final_hist = 255
    im_aux = im
    if space == 'HSV':
        im_aux = color.rgb2hsv(im)
        final_hist = 1
    elif space == 'YCBCR':
        im_aux = color.rgb2ycbcr(im)


    if channel == 'ch1':
        his = np.histogram(im_aux[:, :, 0], bins=255, range=(init_his, final_hist))[0]
    elif channel == 'ch2':
        his = np.histogram(im_aux[:, :, 1], bins=255, range=(init_his, final_hist))[0]
    elif channel == 'ch3':
        his = np.histogram(im_aux[:, :, 2], bins=255, range=(init_his, final_hist))[0]
    bins = np.histogram(im_aux[:, :, 0], bins=255, range=(init_his, final_hist))[1]

    return bins, his, init_his, final_hist


def visualize_histogram(tittle,his1, his2, his3, initial, final,crop_img_signal):


    fig, channel = plt.subplots(1, 3,figsize=(16, 9), sharey=True)
    channel[0].bar(np.linspace(initial, final, 255)[:-2], his1[1:-1], color='r', width=0.8 * (initial - final) / 255 , label='Ch1')
    channel[1].bar(np.linspace(initial, final, 255)[:-2], his2[1:-1], color='g', width=0.8 * (initial - final) / 255 , label='Ch2')
    channel[2].bar(np.linspace(initial, final, 255)[:-2], his3[1:-1], color='b', width=0.8 * (initial - final) / 255 , label='Ch3')

    data_channel1 = crop_img_signal.ravel()
    data_channel1 = data_channel1[data_channel1 != 0]
    data_channel1 = data_channel1[data_channel1 != 1]  # Removes background pixels (intensities 0 and 1)

    # Fit GMM
    gmm = GaussianMixture(n_components=6)
    gmm = gmm.fit(X=np.expand_dims(crop_img_signal, 1))

    # Evaluate GMM
    gmm_x = np.linspace(0, 253, 256)
    gmm_y = np.exp(gmm.score_samples(gmm_x.reshape(-1, 1)))

    # Plot histograms and gaussian curves
    channel[0].plot(gmm_x, gmm_y, color="crimson", lw=4, label="GMM")

    channel[0].set_ylabel("Frequency")
    channel[0].set_xlabel("Pixel Intensity")
    channel[1].set_ylabel("Frequency")
    channel[1].set_xlabel("Pixel Intensity")
    channel[2].set_ylabel("Frequency")
    channel[2].set_xlabel("Pixel Intensity")
    channel[0].legend()
    channel[1].legend()
    channel[2].legend()

    fig.suptitle(tittle)
    plt.show()

def getThresholds_filing_ratio(database_info):
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