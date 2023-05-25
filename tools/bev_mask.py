import cv2

TEST_NAME = "TEST_0"

array = cv2.imread("/home/aisyslab/DanielM/carla-scripts/_out/TEST_1/sem/sem_  8650.jpg")
mask = cv2.imread('./tools/binary_bev_mask.jpg',0)
res = cv2.bitwise_and(array,array,mask = mask)

cv2.imwrite("./_out/bev_mask_test_2.jpg", res)

cv2.imshow('masked', res)
cv2.waitKey()