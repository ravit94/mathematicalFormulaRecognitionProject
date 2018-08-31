from preprocessing.OtsuMethod import OtsuMethod
from preprocessing.BoundingBoxes import BoundingBoxes
from SymbolRecognition.SymbolRecognition import SymbolRecognition
from SymbolRecognition.ConvertStringToLatexFormat import ConvertStringToLatexFormat
from StructureAnalysis.StructureAnalysis import StructureAnalysis
import shutil
import os

imagePath = "example.PNG"
otsu = OtsuMethod()
boundingBoxes = BoundingBoxes()
symbolRecognition = SymbolRecognition()
convertStringToLatexFormat = ConvertStringToLatexFormat()
structureAnalysis = StructureAnalysis()
# get the path to rows directory
binaryImageDirPath = otsu.ConvertToBinaryImage(imagePath)
rows = os.listdir(binaryImageDirPath)
for row in rows:
    res = symbolRecognition.ocr(binaryImageDirPath+ "//" + row)
    if res == '':
        boxes = boundingBoxes.SegmentImageToBoxes(binaryImageDirPath + "//" + row)
        print(structureAnalysis.StructureAnalysis(boxes))
    else:
        print(res)
# delete the temporary directory
shutil.rmtree(binaryImageDirPath)