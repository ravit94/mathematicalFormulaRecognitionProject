from preprocessing.OtsuMethod import OtsuMethod
from preprocessing.BoundingBoxes import BoundingBoxes
from SymbolRecognition.SymbolRecognition import SymbolRecognition
from SymbolRecognition.ConvertStringToLatexFormat import ConvertStringToLatexFormat
import shutil
import os

imagePath = "example.PNG"
otsu = OtsuMethod()
boundingBoxes = BoundingBoxes()
symbolRecognition = SymbolRecognition()
convertStringToLatexFormat = ConvertStringToLatexFormat()
binaryImageDirPath = otsu.ConvertToBinaryImage(imagePath)
rows = os.listdir(binaryImageDirPath)
for row in rows:
    res = symbolRecognition.ocr(binaryImageDirPath+ "//" + row)
    if res == '':
        boxes = boundingBoxes.SegmentImageToBoxes(binaryImageDirPath + "//" + row)
        print (boxes)
    else:
        print (res)

shutil.rmtree(binaryImageDirPath)