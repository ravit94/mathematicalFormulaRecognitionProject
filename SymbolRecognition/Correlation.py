import os
from PIL import Image

class Correlation(object):
    """
    Correlation method aim is to find the correlation between BB to one of the templates.
    """

    def __init__(self):
        super(Correlation, self).__init__()
        self.mostCOmmon = ["frac.png", "infinity.png", "infinity2.png", "integral.png", "pi.png"]

    def FindCorrelationCoefficient(self, bb):
        """
        find the correlation coefficient between given BB to each one of the templates
        and return the max.
        :param bb: one of the boundingBoxes
        :type bb: Image
        """
        size = 500
        imageA = Image.open(bb)
        # a dictionary that save the error of each template
        gaps = {}
        # Resize it.
        img = imageA.resize((size, size), Image.BILINEAR)
        templates = os.listdir("Templates")
        # go over all the templates and insert to gaps, start with the most common
        for template in self.mostCOmmon:
            imageB = Image.open("Templates\\" + template)
            diff = self.CompareImages(imageA, imageB)
            templates.remove(template)
            # find the smallest error.
            if diff < 20:
                return template
        for template in templates:
            imageB = Image.open("Templates\\" + template)
            diff = self.CompareImages(imageA, imageB)
            # find the smallest error.
            if diff < 20:
                return template
        # return the name of the most similar template.
        return None

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
        imageA = Image.open(bb)
        path = "Digits&Letters\\" + symbol
        if not os.path.isdir(path):
            return False
        templates = os.listdir(path)
        for template in templates:
            if not os.path.isfile(path + "\\" + template):
                return False
            imageB = Image.open(path + "\\" + template)
            diff = self.CompareImages(imageA, imageB)
            # find the smallest error.
            if diff < 18:
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