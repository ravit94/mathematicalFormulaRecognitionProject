
class StructureAnalysis(object):
    """
    StructureAnalysis method aim is to find the relationship between symbols.
    """

    def __init__(self):
        super(StructureAnalysis, self).__init__()
        self.spacialList = ["frac", "int", "sqrt", "leftPar", "sum"]
        self.exception = ["=", "+"]

    def Preprocessing(self, boxes):
        """
        find the spacial relationship between given BB dictionary and add elements to help analysis process.
        :param boxes: all the information about the boundingBoxes in the current row.
        :type boxes: Dictionary
        """
        i = 0
        while i != len(boxes):
            if boxes[i][1]["value"] == '\\frac':
                lastXcoordinate = 0
                data = {"maxY": 1000, "minY": 0, "xCoordinate": 0, "yCoordinate": 0, "isFirst": False}
                xStartBound = boxes[i][1]["x"]
                xEndBound = boxes[i][1]["x"] + boxes[i][1]["w"]
                for j in range(i, len(boxes)):
                    # add the bb that above or below the fracture line.
                    if (boxes[j][1]["x"] > xStartBound and boxes[j][1]["x"] + boxes[j][1]["w"] <= xEndBound) or boxes[j][1]["x"] == xStartBound:
                        if boxes[j][1]["y"] < boxes[i][1]["y"] and boxes[j][1]["y"] < data["maxY"]:
                            if not data["isFirst"]:
                                data["xCoordinate"] = boxes[j][1]["x"]
                                data["yCoordinate"] = boxes[j][1]["y"]
                                data["isFirst"] = True
                            data["maxY"] = boxes[j][1]["y"]
                        elif boxes[j][1]["y"] > boxes[i][1]["y"] and boxes[j][1]["y"] + boxes[j][1]["h"] > data["minY"]:
                            data["minY"] = boxes[j][1]["y"] + boxes[j][1]["h"]
                        lastXcoordinate = boxes[j][1]["x"]
                    # if not the first bb - break from loop.
                    elif boxes[j][1]["x"] > xStartBound:
                        break
                if lastXcoordinate == boxes[i][1]["x"]:
                    boxes[i][1]["value"] = "-"
                    continue
                boxes.insert(i, (xStartBound, {"x": data["xCoordinate"], "y":  data["yCoordinate"],
                                               "h":  data["minY"] - data["maxY"],
                                               "w": boxes[i][1]["w"], "value": "frac {}".format(lastXcoordinate)}))
                i += 1
            if boxes[i][1]["value"] == '\int_':
                lastXcoordinate = 0
                for j in range(i, len(boxes)):
                    # add the bb that part of the integral.
                    if boxes[j][1]["value"] != "d":
                        continue
                    # content of integral end with "dx".
                    elif boxes[j][1]["value"] == "d":
                        if boxes[j + 1][1]["value"] == "x":
                            lastXcoordinate = boxes[j+1][1]["x"]
                        break
                boxes.insert(i, (boxes[i][1]["x"], {"x":boxes[i][1]["x"], "y": boxes[i][1]["y"], "h": boxes[i][1]["h"],
                                "w": boxes[j + 1][1]["w"] + boxes[j + 1][1]["x"] - boxes[i][1]["x"],
                                "value": "int {}".format(lastXcoordinate)}))
                i += 1
            if boxes[i][1]["value"] == '\\sqrt':
                lastXcoordinate = 0
                xStartBound = boxes[i][1]["x"]
                xEndBound = boxes[i][1]["x"] + boxes[i][1]["w"]
                for j in range(i, len(boxes)):
                    # add the bb that inside the sqrt.
                    if (boxes[j][1]["x"] > xStartBound and boxes[j][1]["x"] + boxes[j][1]["w"] < xEndBound) or \
                            boxes[j][1]["x"] == xStartBound:
                        lastXcoordinate = boxes[j][1]["x"]
                    # if not the first bb - break from loop.
                    elif boxes[j][1]["x"] > xStartBound:
                        break
                boxes.insert(i, (xStartBound, {"x": boxes[i][1]["x"], "y": boxes[i][1]["y"],
                                               "h": boxes[i][1]["h"],
                                               "w": boxes[i][1]["w"], "value": "sqrt {}".format(lastXcoordinate)}))
                i += 1
            if boxes[i][1]["value"] == '\left ( ':
                lastXcoordinate = 0
                xStartBound = boxes[i][1]["x"]
                for j in range(i, len(boxes)):
                    # add the bb that inside the Parenthesis.
                    if boxes[j][1]["value"] == '\\right )' and abs(boxes[j][1]["y"] - boxes[i][1]["y"]) < 2 :
                        lastXcoordinate = boxes[j][1]["x"]
                        break
                boxes.insert(i, (xStartBound, {"x": boxes[i][1]["x"], "y": boxes[i][1]["y"],
                                               "h": boxes[i][1]["h"],
                                               "w": boxes[j][1]["x"] - xStartBound,
                                               "value": "leftPar {}".format(lastXcoordinate)}))
                i += 1
            if boxes[i][1]["value"] == '\sum':
                lastXcoordinate = 0
                xStartBound = boxes[i][1]["x"]
                xEndBound = boxes[i][1]["x"] + boxes[i][1]["w"] +20
                for j in range(i, len(boxes)):
                    # add the bb that above or below the fracture line.
                    if (boxes[j][1]["x"] >= xStartBound and boxes[j][1]["x"] + boxes[j][1]["w"] < xEndBound) or boxes[j][1]["x"] == xStartBound:
                        lastXcoordinate = boxes[j][1]["x"]
                    # if not the first bb - break from loop.
                    elif boxes[j][1]["x"] > xEndBound:
                        break
                boxes.insert(i, (xStartBound, {"x": boxes[i][1]["x"], "y": boxes[i][1]["y"],
                                               "h": boxes[i][1]["h"], "w": boxes[j][1]["x"] - xStartBound,
                                               "value": "sum {}".format(lastXcoordinate)}))
                i += 1
            if boxes[i][1]["value"] == 'l' and i < (len(boxes) - 1):
                if boxes[i + 1][1]["value"] == '\\cdot':
                    boxes[i][1]["value"] = "i"
                    boxes.remove(boxes[i + 1])
            i += 1
        return boxes

    def _NextIndex(self, box, boxes):
        """
        return the next index
        :param box: first BB
        :type box: Dictionary
        """
        required = box[1]["value"].split(" ")[1]
        for i in range(boxes.index(box), len(boxes)):
            if boxes[i][1]["x"] == required:
                return i
        return None



    def StructureAnalysis(self, boxes):
        """
        find the relationship between given BB dictionary that represent row in the image ans return
        string in Latex format of the current row.
        :param boxes: all the information about the boundingBoxes in the current row.
        :type boxes: Dictionary
        """
        return self.RecAnalysis(self.Preprocessing(boxes))

    def RecAnalysis(self, boxes):
        """
        find the relationship between given BB dictionary that represent row in the image ans return
        string in Latex format of the current row.
        :param boxes: all the information about the boundingBoxes in the current row.
        :type boxes: Dictionary
        """
        flag = False
        resultString = ""
        self.mapToFanc = {"frac": self._FractureHandling, "int": self._IntegralHandling, "sqrt": self._SqrtHandling,
                          "leftPar": self._ParenthesisHandling, "sum": self._SumHandling}
        i = 0
        while i < len(boxes):
            if boxes[i][1]["value"].split(" ")[0] in self.spacialList:
                lastXcoordinate = int(boxes[i][1]["value"].split(" ")[1])
                string, end, flag = self.mapToFanc[boxes[i][1]["value"].split(" ")[0]](boxes, i+1, lastXcoordinate)
                resultString = resultString + string
                i = end
            else:
                # recognize exponent relation
                if i > 0 and not flag:
                    ref = boxes[i-1][1]
                    if ref["value"] == '\\right )':
                        ref["y"] -= 5
                    if boxes[i][1]["y"] + 0.6 * boxes[i][1]["h"] < ref["y"] + 0.6 * ref["h"] and \
                            abs((boxes[i][1]["y"] + boxes[i][1]["h"]) - (ref["y"] + ref["h"])) > 10 and \
                            boxes[i][1]["value"] not in self.exception and ref["value"] not in self.exception:
                        if boxes[i][1]["value"] == "-":
                            if i < len(boxes) - 1:
                                if not ( boxes[i+1][1]["y"] + 0.6 * boxes[i+1][1]["h"] < ref["y"] + 0.6 * ref["h"] and \
                            abs((boxes[i+1][1]["y"] + boxes[i+1][1]["h"]) - (ref["y"] + ref["h"])) > 10 and \
                            boxes[i][1]["value"] not in self.exception and ref["value"] not in self.exception):
                                    flag = True
                                    continue
                        resultString = resultString + "^{"
                        j = i
                        while j != len(boxes):
                            if boxes[j][1]["value"].split(" ")[0] in self.spacialList:
                                lastXcoordinate = int(boxes[j][1]["value"].split(" ")[1])
                                string, end , flag = self.mapToFanc[boxes[j][1]["value"].split(" ")[0]](boxes, j + 1,
                                                                                                 lastXcoordinate)
                                resultString = resultString + string
                                j = end
                                continue
                            if (boxes[j][1]["y"] + 0.6 * boxes[j][1]["h"] < ref["y"] + 0.6 * ref["h"]) and \
                                    boxes[j][1]["value"] not in self.exception  \
                                    and abs((boxes[j][1]["y"] + boxes[j][1]["h"]) - (ref["y"] + ref["h"])) > 5:
                                resultString = resultString + boxes[j][1]["value"]
                            else:
                                break
                            j += 1
                        i = j
                        resultString = resultString + "}"
                        continue
                if i < (len(boxes) - 1):
                    if abs(boxes[i + 1][1]["x"] - boxes[i][1]["x"]) == 0.5:
                        boxes[i][1]["value"] = "="
                        boxes.remove(boxes[i + 1])
                resultString = resultString + boxes[i][1]["value"]
                flag = False
                i += 1
        return resultString

    def _FractureHandling (self, boxes, start, lastXcoordinate):
        """
        handle the case of fracture, finds the numerator and the denominator and returns a string representing the fraction
        :param boxes: all the information about the boundingBoxes in the fracture.
        :type boxes: Dictionary
        :param start: the index of the first BB.
        :type start: int
        :param lastXcoordinate: the index of the last BB.
        :type lastXcoordinate: int
        """
        numeratorDict = []
        denominatorDict = []
        i = start
        while boxes[i][1]["x"] <= lastXcoordinate:
            if boxes[i][1]["value"] == '\\frac':
                i += 1
                continue
            if boxes[i][1]["y"] < boxes[start][1]["y"]:
                numeratorDict.append(boxes[i])
            else:
                denominatorDict.append(boxes[i])
            i += 1
            if i == len(boxes):
                break
        numerator = self.RecAnalysis(numeratorDict)
        denominator = self.RecAnalysis(denominatorDict)
        return "\\frac{" + numerator + "}{" + denominator + "}" , i, False

    def _IntegralHandling (self, boxes, start, lastXcoordinate):
        """
        handle the case of integral, finds the boundaries and returns a string representing the integral content
        :param boxes: all the information about the boundingBoxes in the integral.
        :type boxes: Dictionary
        :param start: the index of the first BB.
        :type start: int
        :param lastXcoordinate: the index of the last BB.
        :type lastXcoordinate: int
        """
        upperDict = []
        lowerDict = []
        contentDict = []
        i = start
        while boxes[i][1]["x"] < lastXcoordinate:
            if boxes[i][1]["value"] == '\int_':
                i += 1
                continue
            if boxes[i][1]["y"] < boxes[start][1]["y"]:
                upperDict.append(boxes[i])
            elif boxes[i][1]["y"] > boxes[start][1]["y"] + boxes[start][1]["h"] - 30:
                lowerDict.append(boxes[i])
            else:
                while boxes[i][1]["x"] < lastXcoordinate:
                    contentDict.append(boxes[i])
                    i += 1
                break
            i += 1
        if boxes[i][1]["x"] == lastXcoordinate:
            contentDict.append(boxes[i])
        lower = self.RecAnalysis(lowerDict)
        upper = self.RecAnalysis(upperDict)
        content = self.RecAnalysis(contentDict)
        return "\int_{" + lower + "}^{" + upper + "} " + content , i+1, False

    def _SqrtHandling (self, boxes, start, lastXcoordinate):
        """
        handle the case of Sqrt,  finds the boundaries and returns a string representing the sqrt content
        :param boxes: all the information about the boundingBoxes in the Sqrt.
        :type boxes: Dictionary
        :param start: the index of the first BB.
        :type start: int
        :param lastXcoordinate: the index of the last BB.
        :type lastXcoordinate: int
        """
        i = start + 1
        contentDict = []
        while boxes[i][1]["x"] < lastXcoordinate:
            contentDict.append(boxes[i])
            i += 1
        if boxes[i][1]["x"] == lastXcoordinate:
            contentDict.append(boxes[i])
        content = self.RecAnalysis(contentDict)
        return "\sqrt{" + content + "}", i+1, False

    def _ParenthesisHandling(self, boxes, start, lastXcoordinate):
        """
        handle the case of Parenthesis, finds the boundaries and returns a string representing the Parenthesis content
        :param boxes: all the information about the boundingBoxes in the Parenthesis.
        :type boxes: Dictionary
        :param start: the index of the first BB.
        :type start: int
        :param lastXcoordinate: the index of the last BB.
        :type lastXcoordinate: int
        """
        i = start + 1
        contentDict = []
        upper = []
        lower = []
        while boxes[i][1]["x"] < lastXcoordinate:
            contentDict.append(boxes[i])
            i += 1
        j = 1
        # try to recognize binom relation
        if len(contentDict) > 1:
            if (contentDict[j - 1][1]["x"] - contentDict[j][1]["x"]) < 4 and \
                    (contentDict[j - 1][1]["y"] + contentDict[j - 1][1]["h"]) < contentDict[j][1]["y"]:
                upper.append(contentDict[j - 1])
                lower.append(contentDict[j])
                j += 1
                while j < len(contentDict):
                    if contentDict[j][1]["y"] > (upper[0][1]["y"] + upper[0][1]["h"]):
                        lower.append(contentDict[j])
                    else:
                        upper.append(contentDict[j])
                    j += 1
                up = self.RecAnalysis(upper)
                low = self.RecAnalysis(lower)
                content = "\\binom{" + up + "}{" + low + "}"
                return content, i + 1, True

        content = self.RecAnalysis(contentDict)
        return "(" + content + ")", i+1, False

    def _SumHandling(self, boxes, start, lastXcoordinate):
        """
        handle the case of sum, finds the boundaries and returns a string representing the sum
        :param boxes: all the information about the boundingBoxes in the fracture.
        :type boxes: Dictionary
        :param start: the index of the first BB.
        :type start: int
        :param lastXcoordinate: the index of the last BB.
        :type lastXcoordinate: int
        """
        upperDict = []
        lowerDict = []
        i = start
        while boxes[i][1]["x"] <= lastXcoordinate:
            if boxes[i][1]["value"] == '\sum':
                i += 1
                continue
            if boxes[i][1]["y"] < boxes[start][1]["y"]:
                upperDict.append(boxes[i])
            elif boxes[i][1]["y"] > boxes[start][1]["y"] + boxes[start][1]["h"]:
                lowerDict.append(boxes[i])
            if boxes[i][1]["x"] == lastXcoordinate:
                break
            i += 1
        lower = self.RecAnalysis(lowerDict)
        upper = self.RecAnalysis(upperDict)
        if lower.__contains__("^{-}"):
            lower = lower.replace("^{-}", "=")
        return "\sum_{" + lower + "}^{" + upper + "} ", i + 1 , True
