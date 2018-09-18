from preprocessing.OtsuMethod import OtsuMethod
from preprocessing.BoundingBoxes import BoundingBoxes
from SymbolRecognition.SymbolRecognition import SymbolRecognition
from SymbolRecognition.ConvertStringToLatexFormat import ConvertStringToLatexFormat
from StructureAnalysis.StructureAnalysis import StructureAnalysis
import shutil
import sys
import os

arglist = sys.argv
imagePath = arglist[1]
list= ["C:\\Users\\ravir\\Desktop\\tests\\bi.PNG", "C:\\Users\\ravir\\Desktop\\tests\\binom.PNG", "C:\\Users\\ravir\\Desktop\\tests\\co.PNG",
       "C:\\Users\\ravir\\Desktop\\tests\\eq.PNG", "C:\\Users\\ravir\\Desktop\\tests\\ex1.PNG", "C:\\Users\\ravir\\Desktop\\tests\\ex2.PNG",
       "C:\\Users\\ravir\\Desktop\\tests\\ex3.PNG", "C:\\Users\\ravir\\Desktop\\tests\\g.png", "C:\\Users\\ravir\\Desktop\\tests\g15.png",
       "C:\\Users\\ravir\\Desktop\\tests\g12.png", "C:\\Users\\ravir\\Desktop\\tests\g17.png", "C:\\Users\\ravir\\Desktop\\tests\sum.PNG", "C:\\Users\\ravir\\Desktop\\tests\sum.PNG"]
otsu = OtsuMethod()
boundingBoxes = BoundingBoxes()
symbolRecognition = SymbolRecognition()
convertStringToLatexFormat = ConvertStringToLatexFormat()
structureAnalysis = StructureAnalysis()
# get the path to rows directory
binaryImageDirPath = otsu.ConvertToBinaryImage(imagePath)
rows = os.listdir(binaryImageDirPath)
resultString = ""
for row in rows:
    res = symbolRecognition.ocr(binaryImageDirPath+ "//" + row)
    if res == '' or res.__contains__("\n"):
        boxes = boundingBoxes.SegmentImageToBoxes(binaryImageDirPath + "//" + row)
        resultString = resultString + structureAnalysis.StructureAnalysis(boxes) + "\n"
    else:
        resultString = resultString + res + "\n"
# delete the temporary directory
shutil.rmtree(binaryImageDirPath)
convertStringToLatexFormat.CreateLatexFile(resultString, imagePath)