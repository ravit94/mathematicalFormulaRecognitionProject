import os
from PIL import Image

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
        # a dictionary that save the error of each template/
        gaps = {}
        # Resize it.
        img = imageA.resize((size, size), Image.BILINEAR)
        templates = os.listdir("Templates")
        # go over all the templates and insert to gaps.
        for template in templates:
            imageB = Image.open("Templates\\" + template)
            diff = self.CompareImages(imageA, imageB)
            gaps.update({template: diff})
        # find the smallest error.
        minDiff = min(gaps.items(), key = lambda x: x[1])
        # if the smallest error is bigger then 20 so None of the template is similar enough.
        if minDiff[1] > 20:
            return None
        # return the name of the most similar template.
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
        # we save the upper as dabble.
        if symbol.isupper():
            symbol = symbol + symbol
        path = "LettersDigits\\" + symbol + ".png"
        # check if exist.
        if not os.path.isfile(path):
            return False
        # open the images.
        imageA = Image.open(bb)
        imageB = Image.open(path)
        diff = self.CompareImages(imageA, imageB)
        # check if the two given images are equal.
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
        # calculate the correlation coefficient.
        for p1, p2 in pairs:
            for x, y in zip(p1, p2):
                dif = dif + abs(x - y)

        ncomponents = img.size[0] * img2.size[1] * 3
        diff = (dif / 255.0 * 100) / ncomponents
        return diff