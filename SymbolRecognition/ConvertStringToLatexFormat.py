
class ConvertStringToLatexFormat(object):
   """
   BoundingBoxes used to segment binary image into boxes.
   """

   def __init__(self):
      super(ConvertStringToLatexFormat, self).__init__()

   def ConvertToLatexFormat(self, symbol):
      """
      This function receive the symbol that recognized by tesseract
      or by correlation coefficient and return the symbol in latex format.
      :param symbol: recognized by tesseract or by correlation coefficient
      :type symbol: string
      """

      if symbol.startswith('infinity'):
          return 'inf'
      elif symbol.startswith('sigma'):
          return 'sig'

temp = ConvertStringToLatexFormat()
res = temp.ConvertToLatexFormat("infinity234")
print (res)