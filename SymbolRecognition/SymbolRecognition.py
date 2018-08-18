import pytesseract
from PIL import Image
from PIL import ImageFilter
from SymbolRecognition.Correlation import Correlation
class SymbolRecognition(object):
    """
    OtsuMethod used to convert image into binary image.
    """

    def __init__(self):
        super(SymbolRecognition, self).__init__()

    def Recognize(self, BoundingBoxPath):
        """
        try to recognize the content of each BoundingBox by using Tesseract.
        :param BoundingBoxPath: path to the boundingBox image
        :type BoundingBoxPath: string
        """
        # Open the BoundingBox image
        im = Image.open(BoundingBoxPath)
        im.filter(ImageFilter.SHARPEN)
        # Define the command
        correlation = Correlation()
        symbol = correlation.FindCorrelationCoefficient(BoundingBoxPath)
        if  symbol == None :
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
            # Send the image to Tesseract to recognize it.
            tesseractLetter = pytesseract.image_to_string(im, lang='eng', boxes=False,
                                             config='--psm 10 --eom 1 -c tessedit_char_'
                                             'whitelist=-+%ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrtsuvwxyz0123456789')
            if not correlation.IsEqual(BoundingBoxPath, tesseractLetter):
                symbol = correlation.FindCorrelationCoefficient(BoundingBoxPath)
                print(symbol)
            else:
                print (tesseractLetter)
        else:
            print(symbol)