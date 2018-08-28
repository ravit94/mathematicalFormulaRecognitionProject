from preprocessing.OtsuMethod import OtsuMethod
from preprocessing.BoundingBoxes import BoundingBoxes
from SymbolRecognition.SymbolRecognition import SymbolRecognition
from SymbolRecognition.ConvertStringToLatexFormat import ConvertStringToLatexFormat
imagePath = "exp.PNG"
otsu = OtsuMethod()
boundingBoxes = BoundingBoxes()
symbolRecognition = SymbolRecognition()
convertStringToLatexFormat = ConvertStringToLatexFormat()
boxes = boundingBoxes.SegmentImageToBoxes(otsu.ConvertToBinaryImage(imagePath))
for box in boxes:
   print(convertStringToLatexFormat.ConvertToLatexFormat(symbolRecognition.Recognize(box)))