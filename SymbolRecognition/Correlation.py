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
        fine the correlation coefficient between given BB to each one of the templates
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
            # Calculate the height using the same aspect ratio
            widthPercent = (size / float(img.size[0]))
            height = int((float(img.size[1]) * float(widthPercent)))

            # Resize it.
            img2 = imageB.resize((size, height), Image.BILINEAR)
            pairs = zip(img.getdata(), img2.getdata())
            dif = 0
            for p1, p2 in pairs:
                for x, y in zip(p1, p2):
                    dif = dif + abs(x - y)

            ncomponents = img.size[0] * img2.size[1] * 3
            diff = (dif / 255.0 * 100) / ncomponents
            gaps.update({template: diff})
        minDiff = min(gaps.items(), key = lambda x: x[1])
        if minDiff[1] > 20:
            return None
        return minDiff[0]