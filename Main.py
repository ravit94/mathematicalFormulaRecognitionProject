from preprocessing.OtsuMethod import OtsuMethod
from preprocessing.BoundingBoxes import BoundingBoxes
from SymbolRecognition.SymbolRecognition import SymbolRecognition

imagePath = "C:\\Users\\ravir\\PycharmProjects\\FinalProject\\exp.PNG"
otsu = OtsuMethod()
boundingBoxes = BoundingBoxes()
symbolRecognition = SymbolRecognition()
boxes = boundingBoxes.SegmentImageToBoxes(otsu.ConvertToBinaryImage(imagePath))
for box in boxes:
    symbolRecognition.Recognize(box)