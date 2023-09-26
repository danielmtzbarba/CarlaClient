import os
import cv2
import numpy as np
from pathlib import Path


from tqdm import tqdm

from dan.utils import make_folder
from dan.utils.data import get_filenames_list

DIM_BEV_OUT = (64, 64)
MASK = cv2.imread(str(Path("assets") / "binary_bev_mask.jpg"), 0)

def get_test_dirs(dataset_path):
    maps = [ Path(f.path) for f in os.scandir(dataset_path) if f.is_dir() ]
    tests = []
    for map in maps:
        tests.extend([ Path(f.path) for f in os.scandir(map) if f.is_dir() ])
    return tests

def mask_img(img):
    return cv2.bitwise_and(img,img,mask = MASK)

def resize_img(img):
    return cv2.resize(img, DIM_BEV_OUT, interpolation = cv2.INTER_NEAREST)

def remap_segmentation(img):
    h = img.shape[0]
    w = img.shape[1]

    # loop over the image
    for y in range(0, h):
        for x in range(0, w):
            if img.item(y, x) == 0:
                continue
            elif img.item(y, x) == 90:
                img[y, x] = 1
            elif img.item(y, x) == 16:
                img[y, x] =  2
            elif img.item(y, x) == 190:
                img[y, x] = 3
            else:
                img[y, x] = 4

    img[30:35, 32] = 5
    
    return img

def postprocess(img):
    masked = mask_img(img)
    resized = resize_img(masked)
    segmented = remap_segmentation(resized)
    return segmented

def main(dataset_path):

    test_paths = get_test_dirs(dataset_path)
    for test_path in tqdm(test_paths):

        bev_raw_path = test_path / "bev"
        save_bev = make_folder(test_path, "bev2")

        bev_imgs = get_filenames_list(bev_raw_path, ".jpg")
        for bev_img_name in tqdm(bev_imgs):
            bev_img = cv2.imread(str(bev_raw_path / bev_img_name), cv2.IMREAD_GRAYSCALE)
            bev_post = postprocess(bev_img)
            cv2.imwrite(str(save_bev / bev_img_name).replace('.jpg', '.png'), bev_post)

if __name__ == '__main__':
    root_path = Path("/media/aisyslab/ADATA HD710M PRO/DATASETS/Front2BEV/")
    main(root_path)