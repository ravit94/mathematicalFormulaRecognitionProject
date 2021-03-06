import os
from PIL import Image
import cv2
import numpy as np
class Correlation(object):
    """
    Correlation method aim is to find the correlation between BB to one of the templates.
    """

    def __init__(self):
        super(Correlation, self).__init__()
        self.mostCOmmon = ["frac.png", "infinity.png", "infinity2.png", "integral.png", 'sig.png', "pi.png", "rightPar1.png", "leftPar1.png"]
        self.minDif = 100000
        self.minTemplate = "?"

    def FindCorrelationCoefficient(self, bb):
        """
        find the correlation coefficient between given BB to each one of the templates
        and return the max.
        :param bb: one of the boundingBoxes
        :type bb: Image
        """
        size = 500
        imageA = cv2.imread(bb)
        templates = os.listdir("Templates")

        # go over all the templates and insert to gaps, start with the most common
        for template in self.mostCOmmon:
            imageB = cv2.imread("Templates\\" + template)
            diff = self.CompareImages(imageA, imageB)
            templates.remove(template)
            # find the smallest error.
            if diff < 11:
                return template, True
        for template in templates:
            imageB =cv2.imread("Templates\\" + template)
            diff = self.CompareImages(imageA, imageB)
            # find the smallest error.
            if diff < 9.992:
                return template, True
        # return the name of the most similar template.
        return self.minTemplate, False

    def IsEqual(self, bb, symbol):
        """
        Compare the bondingBox to the relevant template
        :param bb: one of the boundingBoxes
        :type bb: Image
        :param symbol: template of the symbol
        :type symbol: string
        """
        # Resize it.
        size = 500
        imageA = cv2.imread(bb)
        path = "Digits&Letters\\" + symbol
        if not os.path.isdir(path):
            return False
        templates = os.listdir(path)
        for template in templates:
            if not os.path.isfile(path + "\\" + template):
                return False
            imageB = cv2.imread(path + "\\" + template)
            diff = self.CompareImages(imageA, imageB)
            # find the smallest error.
            if diff < 9.5:
                return True
        return False

    def CompareImages(self, imageA, imageB):
        """
        Compare two images and return the difference between them.
        :param imageA: image one to compare
        :type imageA: Image
        :param imageB: image two to compare
        :type imageB: Image
        """
        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
        (H, W) = grayA.shape
        grayB = cv2.resize(grayB, (W, H))
        err = np.sum((grayA.astype("float") - grayB.astype("float")) ** 2)
        err /= float(grayA.shape[0] * grayA.shape[1])

        return err / 1000

    def FindMostSimilarTemplate(self, bb):
        """
        find the correlation coefficient between given BB to each one of the templates
        and return the max.
        :param bb: one of the boundingBoxes
        :type bb: Image
        """
        size = 500
        imageA = cv2.imread(bb)
        path = "Digits&Letters\\"
        if not os.path.isdir(path):
            return False
        symbols = os.listdir(path)
        for templates in symbols:
            templateList = os.listdir(path + templates)
            for template in templateList:
                if not os.path.isfile(path + templates + "\\" + template):
                    return False
                imageB = cv2.imread(path + templates + "\\" + template)
                diff = self.CompareImages(imageA, imageB)
                # find the smallest error.
                if diff < 9:
                    return template
                if diff < self.minDif:
                    self.minDif = diff
                    self.minTemplate = templates
        self.minTemplate = self.minTemplate = '?' if self.minDif > 14 else self.minTemplate.split(".")[0]
        return self.minTemplate