from preprocessing.OtsuMethod import OtsuMethod
from preprocessing.BoundingBoxes import BoundingBoxes
from SymbolRecognition.SymbolRecognition import SymbolRecognition
from SymbolRecognition.ConvertStringToLatexFormat import ConvertStringToLatexFormat
from StructureAnalysis.StructureAnalysis import StructureAnalysis
import shutil
import sys
import os

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


arglist = sys.argv
otsu = OtsuMethod()
boundingBoxes = BoundingBoxes()
symbolRecognition = SymbolRecognition()
convertStringToLatexFormat = ConvertStringToLatexFormat()
structureAnalysis = StructureAnalysis()
for file in arglist[1:]:
    imagePath = file
    # get the path to rows directory
    binaryImageDirPath = otsu.ConvertToBinaryImage(imagePath)
    rows = os.listdir(binaryImageDirPath)
    resultString = ""
    for row in rows:
        res = symbolRecognition.ocr(binaryImageDirPath + "//" + row)
        if res == '' or res.__contains__("\n") or hasNumbers(res):
            boxes = boundingBoxes.SegmentImageToBoxes(binaryImageDirPath + "//" + row)
            resultString = resultString + structureAnalysis.StructureAnalysis(boxes) + "\n"
        else:
            resultString = resultString + res + "\n"
    # delete the temporary directory
    shutil.rmtree(binaryImageDirPath)
    convertStringToLatexFormat.CreateLatexFile(resultString, imagePath)