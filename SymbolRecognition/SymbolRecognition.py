import pytesseract
from PIL import Image
from PIL import ImageFilter
import cv2


im = Image.open("C:\\Users\\ravir\\PycharmProjects\\FinalProject\\preprocessing\\x.png")
im.filter(ImageFilter.SHARPEN)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
print(pytesseract.image_to_string(im , lang='eng', boxes=False,config='--psm 10 --eom 3 -c tessedit_char_whitelist=€0123456789'))
print(pytesseract.image_to_string(im, boxes=True))