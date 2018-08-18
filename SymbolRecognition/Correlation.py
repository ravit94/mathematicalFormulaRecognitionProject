import os
from PIL import Image

from scipy import signal


class Correlation(object):
    """
    Correlation method aim is to find the correlation between BB to one of the templates.
    """

    def __init__(self):
        super(Correlation, self).__init__()

    def FindCorrelationCoefficient(self, bb):
        """
        find the correlation coefficient between given BB to each one of the templates
        and return the max.
        :param bb: one of the boundingBoxes
        :type bb: Image
        """
        size = 500
        imageA = Image.open(bb)
        gaps = {}
        # Resize it.
        img = imageA.resize((size, size), Image.BILINEAR)
        templates = os.listdir("Templates")
        for template in templates:
            imageB = Image.open("Templates\\" + template)
            diff = self.CompareImages(imageA, imageB)
            gaps.update({template: diff})
        minDiff = min(gaps.items(), key = lambda x: x[1])
        if minDiff[1] > 20:
            return None
        return minDiff[0]

    def IsEqual(self, bb, symbol):
        """
        Compare to the bondingBox to the relevant template
        :param bb: one of the boundingBoxes
        :type bb: Image
        :param symbol: template of the symbol
        :type symbol: string
        """
        # Resize it.
        size = 500
        if symbol.islower():
            symbol = symbol + symbol
        path = "C:\\Users\\ravir\\PycharmProjects\\FinalProject\\LettersDigits\\" + symbol + ".png"
        if not os.path.isfile(path):
            return False
        imageA = Image.open(bb)
        imageB = Image.open(path)
        diff = self.CompareImages(imageA, imageB)
        if diff > 20:
            return False
        return True

    def CompareImages(self, imageA, imageB):
        """
        Compare two images and return the difference between them.
        :param imageA: image one to compare
        :type imageA: Image
        :param imageB: image two to compare
        :type imageB: Image
        """
        size = 500
        gaps = {}
        # Resize imageA.
        img = imageA.resize((size, size), Image.BILINEAR)
        # Calculate the height using the same aspect ratio
        widthPercent = (size / float(img.size[0]))
        height = int((float(img.size[1]) * float(widthPercent)))

        # Resize ImageB.
        img2 = imageB.resize((size, height), Image.BILINEAR)
        pairs = zip(img.getdata(), img2.getdata())
        dif = 0
        for p1, p2 in pairs:
            for x, y in zip(p1, p2):
                dif = dif + abs(x - y)

        ncomponents = img.size[0] * img2.size[1] * 3
        diff = (dif / 255.0 * 100) / ncomponents
        return diff