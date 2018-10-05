#import cv2
import matplotlib.pyplot as plt
import plotly
import plotly.plotly as py
import plotly.graph_objs as go


def visualize_image(im):
    # Shows the image
    plt.imshow(im)
    plt.show()


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