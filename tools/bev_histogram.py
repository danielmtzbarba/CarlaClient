import cv2
import matplotlib.pyplot as plt

from random import randint

from pathlib import Path

DATASET_PATH = Path("C:\\Users\\Danie\\OneDrive\\dan\\RESEARCH\\DATASETS\\CARLA_BEV\\TOWN01\\bev")

from dan.torch_utils import ImageDataset

bev_dataset = ImageDataset(DATASET_PATH, imread=cv2.IMREAD_GRAYSCALE)

im = bev_dataset[randint(0, len(bev_dataset)-1)]

print(im.shape)

from dan.utils.graph import imshow_grayscale, histogram_grayscale

#imshow_grayscale(im)

histogram_grayscale(im)

plt.show()

"""
from random import randint
from dan.graph_tools import histogram_grayscale, imshow_grayscale, compare_two_plots, compare_images

def debug(img):
    histogram_grayscale(img, title="Histogram - Raw Segmented Image")
    res = postprocess(img)
    _ , ax1 = histogram_grayscale(res, title="Histogram - Post processed")
    #_ , im1 = imshow_grayscale(res)
 
    cv2.imwrite('debug.png', res)
    res_reloaded = cv2.imread('debug.png', cv2.IMREAD_GRAYSCALE)
    _ , ax2 = histogram_grayscale(res_reloaded, title="Histogram - Post processed, Saved and Loaded")
    compare_images([res, res_reloaded])
   # 
    plt.show()
"""