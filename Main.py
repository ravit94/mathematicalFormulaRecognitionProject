from preprocessing.OtsuMethod import OtsuMethod
from preprocessing.BoundingBoxes import BoundingBoxes
from SymbolRecognition.SymbolRecognition import SymbolRecognition

imagePath = "ex1.PNG"
otsu = OtsuMethod()
boundingBoxes = BoundingBoxes()
symbolRecognition = SymbolRecognition()
boxes = boundingBoxes.SegmentImageToBoxes(otsu.ConvertToBinaryImage(imagePath))
for box in boxes:
   symbolRecognition.Recognize(box)