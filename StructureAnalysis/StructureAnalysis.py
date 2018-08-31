from PIL import Image

class StructureAnalysis(object):
    """
    StructureAnalysis method aim is to find the relationship between symbols.
    """

    def __init__(self):
        super(StructureAnalysis, self).__init__()

    def StructureAnalysis(self, boxes):
        """
        find the relationship between given BB dictionary that represent row in the image ans return
        string in Latex format of the current row.
        :param boxes: all the information about the boundingBoxes in the current row.
        :type boxes: Dictionary
        """
        resultString = ""
        for box in boxes:
            if box[1]["value"] == '\\frac':
                fracDict = []
                xStartBound = box[1]["x"]
                xEndBound = box[1]["x"] + box[1]["w"]
                for bb in boxes:
                    # add the bb that above or below the fracture line.
                    if bb[1]["x"] > xStartBound and bb[1]["x"] + bb[1]["w"] < xEndBound:
                        fracDict.append(bb)
                    # if not the first bb - break from loop.
                    elif bb[1]["x"] != xStartBound:
                        break
                resultString = resultString + self._FractureHandling(fracDict, box[1]["y"])
                for element in fracDict:
                    boxes.remove(element)
            elif box[1]["value"] == '\int_':
                integralDict = []
                xStartBound = box[1]["x"]
                for bb in boxes:
                    # add the bb that above or below the fracture line.
                    if bb[1]["x"] > xStartBound and bb[1]["value"] != "d":
                        integralDict.append(bb)
                    # if not the first bb - break from loop.
                    elif bb[1]["value"] == "d":
                        break
                resultString = resultString + self._IntegralHandling(integralDict, box[1]["y"], box[1]["h"])
                for element in integralDict:
                    boxes.remove(element)
            else:
                resultString = resultString + box[1]["value"]
        return resultString

    def _FractureHandling (self, boxes, yCoordinate):
        """
        handle the case of fracture, finds the numerator and the denominator and returns a string representing the fraction
        :param boxes: all the information about the boundingBoxes in the fracture.
        :type boxes: Dictionary
        :param yCoordinate: the value of y coordinate to distinguish between the numerator and the denominator.
        :type yCoordinate: int
        """
        numeratorDict = []
        denominatorDict = []
        for box in boxes:
            if box[1]["y"] < yCoordinate:
                numeratorDict.append(box)
            else:
                denominatorDict.append(box)
        numerator = self.StructureAnalysis(numeratorDict)
        denominator = self.StructureAnalysis(denominatorDict)
        return "\\frac{" + numerator + "}{" + denominator + "}"

    def _IntegralHandling (self, boxes, yCoordinate, height):
        """
        handle the case of integral, finds the boundaries and returns a string representing the integral content
        :param boxes: all the information about the boundingBoxes in the integral.
        :type boxes: Dictionary
        :param yCoordinate: the value of y coordinate to distinguish between the numerator and the denominator.
        :type yCoordinate: int
        :param height: the height of the integral sigh.
        :type height: int
        """
        upperDict = []
        lowerDict = []
        contentDict = []
        for box in boxes:
            if box[1]["y"] < yCoordinate:
                upperDict.append(box)
            elif box[1]["y"] > yCoordinate + height - 20:
                lowerDict.append(box)
            else:
                contentDict.append(box)
        lower = self.StructureAnalysis(lowerDict)
        upper = self.StructureAnalysis(upperDict)
        content = self.StructureAnalysis(contentDict)

        return "\int_{" + lower + "}^{" + upper + "} " + content