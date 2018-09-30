import pytesseract
from PIL import Image
from PIL import ImageFilter
from SymbolRecognition.Correlation import Correlation
from SymbolRecognition.ConvertStringToLatexFormat import ConvertStringToLatexFormat

class SymbolRecognition(object):
    """
    OtsuMethod used to convert image into binary image.
    """

    def __init__(self):
        super(SymbolRecognition, self).__init__()

    def Recognize(self, BoundingBoxPath):
        """
        Recognize the content of each BoundingBox by using Tesseract or correlation coefficient method.
        :param BoundingBoxPath: path to the boundingBox image
        :type BoundingBoxPath: string
        """
        # Open the BoundingBox image
        im = Image.open(BoundingBoxPath)
        exceptionals = ['-', '+']
        im.filter(ImageFilter.SHARPEN)
        # Define the command
        correlation = Correlation()
        latexFormat = ConvertStringToLatexFormat()
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
        # Send the image to Tesseract to recognize it.
        symbol = pytesseract.image_to_string(im, lang='eng', boxes=False,
                                             config='--psm 10 --eom 1 -c tessedit_char_'
                                                    'whitelist=abcdefghijklmnopqrtsuvwxyz1')
        if correlation.IsEqual(BoundingBoxPath, symbol):
            return latexFormat.ConvertToLatexFormat(symbol)
        # Send the image to Tesseract to recognize it.
        symbol = pytesseract.image_to_string(im, lang='eng', boxes=False,
                                                      config='--psm 10 --eom 1 -c tessedit_char_'
                                                             'whitelist=-+ABCDEFGHIJKLMNPQRSTUVWXYZabcdefghijklmnopqrtsuvwxyz0123456789')
        if not correlation.IsEqual(BoundingBoxPath, symbol) and symbol not in exceptionals:
                symbol = correlation.FindCorrelationCoefficient(BoundingBoxPath)

        return latexFormat.ConvertToLatexFormat(symbol)

    def ocr(self, BoundingBoxPath):
        """
        try to recognize the content of each BoundingBox by using Tesseract in case all the row is text.
        :param BoundingBoxPath: path to the boundingBox image
        :type BoundingBoxPath: string
        """
        # Open the BoundingBox image
        im = Image.open(BoundingBoxPath)
        im.filter(ImageFilter.SHARPEN)
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
        # Send the image to Tesseract to recognize it.
        symbol = pytesseract.image_to_string(im)

        return symbol