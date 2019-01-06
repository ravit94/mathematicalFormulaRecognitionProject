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
files = os.listdir(arglist[1])
otsu = OtsuMethod()
boundingBoxes = BoundingBoxes()
symbolRecognition = SymbolRecognition()
convertStringToLatexFormat = ConvertStringToLatexFormat()
structureAnalysis = StructureAnalysis()
for file in files:
    imagePath = arglist[1] + "\\" + file
    # get the path to rows directory
    binaryImageDirPath = otsu.ConvertToBinaryImage(imagePath)
    if not binaryImageDirPath:
        print ("Can't find relevant content in the image")
        break
    rows = os.listdir(binaryImageDirPath)
    resultString = ""
    for row in rows:
        res = symbolRecognition.ocr(binaryImageDirPath + "//" + row)
        if res == '' or res.__contains__("\n") or hasNumbers(res):
            boxes = boundingBoxes.SegmentImageToBoxes(binaryImageDirPath + "//" + row)
            resultString = resultString + "\n\\begin{align*}" +  structureAnalysis.StructureAnalysis(boxes)  + "\n\\end{align*}\n"
        else:
            resultString = resultString + res + "\n"
    # delete the temporary directory
    shutil.rmtree(binaryImageDirPath)
    convertStringToLatexFormat.CreateLatexFile(resultString, imagePath)