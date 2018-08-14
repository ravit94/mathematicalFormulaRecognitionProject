import numpy as np
import cv2
import sys


im = cv2.imread('exe_bin.PNG')
im[im == 255] = 1
im[im == 0] = 255
im[im == 1] = 0
im2 = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(im2, 127, 255, 0)
im3, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for i in range(0, len(contours)):
   cnt = contours[i]
   x, y, w, h = cv2.boundingRect(cnt)
   letter = im[y:y + h, x:x + w]

   cv2.imwrite(str(i)+'2.png', letter)
