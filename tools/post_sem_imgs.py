import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

RESULTS_PATH = Path("C:\\Users\\Danie\\OneDrive\\dan\\RESEARCH\\DATASETS\\CARLA_BEV")

TEST_NAME = "TOWN01"
DIM_BEV = (64, 64)

TEST_PATH = RESULTS_PATH / TEST_NAME

RGB_IMG_PATH = TEST_PATH / "rgb"
SEM_IMG_PATH = TEST_PATH / "sem"
BEV_SAVE_PATH = TEST_PATH / "bev"

mask = cv2.imread(str(Path("tools") / "binary_bev_mask.jpg"), 0)
kernel = np.ones((7,7),np.uint8)
mask_v2 = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
MASK = cv2.morphologyEx(mask_v2, cv2.MORPH_CLOSE, kernel)


def list_test_imgs():
    rgb_lst = os.listdir(RGB_IMG_PATH)
    sem_lst = os.listdir(SEM_IMG_PATH)
    lst = []
    for im in rgb_lst:
        if im in sem_lst:
            lst.append(im)
        else:
            os.remove(str(RGB_IMG_PATH / im))
    return lst

def load_img(img_path):
    return cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

def mask_img(img):
    return cv2.bitwise_and(img,img,mask = MASK)

def resize_img(img):
    return cv2.resize(img, DIM_BEV, interpolation = cv2.INTER_NEAREST)

def two_tag_segmentation(img):
    h = img.shape[0]
    w = img.shape[1]

    # loop over the image
    for y in range(0, h):
        for x in range(0, w):
            # threshold the pixel
            if img.item(y, x) == 0:
                continue
            elif img.item(y, x) == 90:
                img[y, x] = 255
            elif img.item(y, x) == 16:
                img[y, x] = 50
            else:
                img[y, x] = 128
    return img

def postprocess(img):
    masked = mask_img(img)
    resized = resize_img(masked)
    segmented = two_tag_segmentation(resized)
    return segmented

from random import randint
from dan.graph_tools import histogram_grayscale, imshow_grayscale, compare_two_plots, compare_images

def debug(img):
    histogram_grayscale(img, title="Histogram - Raw Segmented Image")
    res = postprocess(img)
    _ , ax1 = histogram_grayscale(res, title="Histogram - Post processed")
    #_ , im1 = imshow_grayscale(res)

    with open('debug.npy', 'wb') as f:
        np.save(f, res)

    with open('debug.npy', 'rb') as f:
        res_reloaded = np.load(f)

    _ , ax2 = histogram_grayscale(res_reloaded, title="Histogram - Post processed, Saved and Loaded")
    compare_images([res, res_reloaded])
   # 
    plt.show()

   
DEBUG = False

if __name__ == '__main__':
    img_lst = list_test_imgs()
    #
    if DEBUG:
        img_lst = [img_lst[randint(0, len(img_lst) - 1)]]
    #
    for img_name in img_lst:
        img_path = SEM_IMG_PATH / img_name
        img = load_img(str(img_path))
        res = postprocess(img)
        #
        if DEBUG:
            debug(img)
        else:
            img_name = img_name[:-4]
            with open(str(BEV_SAVE_PATH  / img_name) + '.npy', 'wb') as f:
                np.save(f, res)
        #