import numpy as np
import cv2

TEST_NAME = "TEST_2"

array = cv2.imread("/home/dan/GitHub/carla-scripts/_out/TEST_2/sem/sem_0.jpg")
mask = cv2.imread("/home/dan/GitHub/carla-scripts/tools/binary_bev_mask.jpg", 0)

kernel = np.ones((7,7),np.uint8)

mask_v2 = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask_v2 = cv2.morphologyEx(mask_v2, cv2.MORPH_CLOSE, kernel)

res = cv2.bitwise_and(array,array,mask = mask_v2)


cv2.imwrite("./tools/test_res_masked.jpg", res)

cv2.imshow('masked', res)
cv2.waitKey(0)