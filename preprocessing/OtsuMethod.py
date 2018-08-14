import cv2 as cv

img = cv.imread('exe.PNG', 0)
ret, binaryImage = cv.threshold(img, 127, 255, cv.THRESH_BINARY_INV)
cv.imwrite("exe_bin.PNG", binaryImage)
