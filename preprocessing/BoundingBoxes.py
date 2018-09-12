import cv2
from SymbolRecognition.SymbolRecognition import SymbolRecognition
import collections
import os
import shutil

class BoundingBoxes(object):
   """
   BoundingBoxes used to segment binary image into boxes.
   """

   def __init__(self):
      super(BoundingBoxes, self).__init__()
      self.symbolRecognition = SymbolRecognition()
      # openCV return the inside of this symbols as another BB so we will skip over them.
      self.skipOnceList = ["e", "d", "\\alpha", "\lambda", "0", "6", "9", "a", "b", "g", "o", "p", "O", "P", "Q", "A"]
      self.skipTwiceList = ["\infty", "\\Theta", "8", "B", "\\beta"]
      # number of times we need to skip
      self.skip = 0

   def SegmentImageToBoxes(self, binaryImagePath):
      """
      Segment the given image to separate bounding boxes.
      :param binaryImagePath: path to the binary image we want to segment
      :type binaryImagePath: string
      """
      # Open the binary image.
      image = cv2.imread(binaryImagePath)
      # Convert the white pixels to black and the blck to white.
      image[image == 255] = 1
      image[image == 0] = 255
      image[image == 1] = 0
      im2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
      ret, thresh = cv2.threshold(im2, 127, 255, 0)
      # Find all the contours using openCV function.
      im3, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      boundingBoxes = {}
      directory = ""
      #ToDo - check if the boundongBoxes are atomic.
      # for each boundingBoxes - save as image.
      for i in range(1, len(contours)):
         if self.skip > 0:
            self.skip = self.skip -1
            continue
         currentBoundingBox = contours[i]
         # The coordinate of the boundingBoxes.
         x, y, w, h = cv2.boundingRect(currentBoundingBox)
         # Crop each box in the image and save it.
         letter = image[y:y + h, x:x + w]
         file_path = "C:/temp/" + str(i) + '.png'
         directory = os.path.dirname(file_path)
         try:
            os.stat(directory)
         except:
            os.mkdir(directory)
            # all the information about this boundingBox
         cv2.imwrite(file_path, letter)
         value = self.symbolRecognition.Recognize(file_path)
         if value == '\sum':
            x -= 5
         boundingBoxes.update({x: {"x": x, "y": y, "h": h, "w": w, "value": value}})
         if value in self.skipOnceList:
            self.skip = 1
         elif value in self.skipTwiceList:
            self.skip = 2
      shutil.rmtree(directory)
      # Return array of boundingBoxes sorted by
      return sorted(boundingBoxes.items())

