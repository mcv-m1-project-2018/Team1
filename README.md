# Team1
TRAFFIC SIGN DETECTION

The goal of this project is to apply segmentation to a sample of different images.
With it, the code will detect some traffic signals in the images and extract their information in order to recognize them.
Different color spaces for mask generation have been used, including YCbCr, hsv and lab.

GETTING STARTED

These instructions will get you a copy of the project up and running on your local machine for testing purposes. 

PREREQUISITES

The following packages must be installed in order to run the code:

- pyramid
- numpy
- imageio
- cv2
- random
- matplotlib
- skimage
- docopt
- sklearn
- plotly
- fnmatch

INSTALLING

We will use Python 3.6 as the interpreter. All the images given shall be located in the same folder (train folder for the training images
and test folder for the test images).


RUNNING THE TESTS

Execute traffic_sign_model.py file. Arguments:

-images_dir Directory with sample images and annotations. Default: ./train/
-output_dir Directory where to store output masks, etc. Default: ./results/
-test_dir Directory with the test split images. Default: ./test/
-pixelMethod Colour space used for creating the masks (YCbCr, hsv or lab). 
-windowMethod Window method used for detecting signals.

AUTHORS
Cara Roca, David
Fuentes López, Daniel
Rodríguez Orihuela, Andreu J
