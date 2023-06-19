import cv2
import matplotlib.pyplot as plt

from random import randint

from pathlib import Path

DATASET_PATH = Path("C:\\Users\\Danie\\OneDrive\\dan\\RESEARCH\\DATASETS\\CARLA_BEV\\TOWN01\\bev")

from dan.torch_utils import ImageDataset

bev_dataset = ImageDataset(DATASET_PATH, imread=cv2.IMREAD_GRAYSCALE)

im = bev_dataset[randint(0, len(bev_dataset)-1)]

print(im.shape)

from dan.graph_tools import imshow_grayscale, histogram_grayscale

#imshow_grayscale(im)

histogram_grayscale(im)

plt.show()