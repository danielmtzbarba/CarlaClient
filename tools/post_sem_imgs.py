import os
import cv2
import numpy as np

from pathlib import Path

RESULTS_PATH = Path("_out")

TEST_NAME = "TEST_2"
DIM_BEV = (64, 64)

TEST_PATH = RESULTS_PATH / TEST_NAME

SEM_IMG_PATH = TEST_PATH / "sem"

mask = cv2.imread("/home/dan/GitHub/carla-scripts/tools/binary_bev_mask.jpg", 0)
kernel = np.ones((7,7),np.uint8)
mask_v2 = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
MASK = cv2.morphologyEx(mask_v2, cv2.MORPH_CLOSE, kernel)


def list_test_imgs(test_path):
    return os.listdir(test_path)

def load_img(img_path):
    return cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

def mask_img(img):
    return cv2.bitwise_and(img,img,mask = MASK)

def resize_img(img):
    return cv2.resize(img, DIM_BEV, interpolation = cv2.INTER_AREA)

def two_tag_segmentation(img):
    h = img.shape[0]
    w = img.shape[1]
    ROAD_TAG_COLOR =  [128, 63, 127]
    BLACK = [0, 0, 0]

    # loop over the image
    for y in range(0, h):
        for x in range(0, w):
            # threshold the pixel
            if np.array_equiv(img[y, x], BLACK):
                continue
            elif img.item(y, x, 0) >  139 and img.item(y, x, 0) < 143:
                img[y, x] = [0, 0, 255]
            else:
                img[y, x] = (255, 255, 255) if img.item(y, x, 0) >  126 and img.item(y, x, 0) < 130 else (200, 200, 200)
    return img

def postprocess(img):
    masked = mask_img(img)
    resized = resize_img(masked)
    return two_tag_segmentation(resized)

def main():
    img_lst = list_test_imgs(SEM_IMG_PATH)
    for img_name in [img_lst[0]]:
        img = load_img(str(SEM_IMG_PATH / img_name))
        res = postprocess(img)

    cv2.imwrite("./tools/test_res_masked.jpg", res)

main()