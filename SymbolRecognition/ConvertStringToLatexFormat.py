
class ConvertStringToLatexFormat(object):
   """
   BoundingBoxes used to segment binary image into boxes.
   """

   def __init__(self):
      super(ConvertStringToLatexFormat, self).__init__()

   def ConvertToLatexFormat(self, symbol):
      """
      This function receive the symbol that recognized by Tesseract
      or by correlation coefficient and return the symbol in latex format.
      :param symbol: recognized by Tesseract or by correlation coefficient
      :type symbol: string
      """
      latexFormat = {'alpha': '\\alpha','beta':'\\beta','bigger':'>','dot':'\cdot','epsilon':'\epsilon',
       'phi':'\phi','frac':'\\frac','gamma':'\gamma','infinity':'\infty','integral':'\int_','lambda':'\lambda',
       'leftArrow':'\leftarrow','leftPar':'\left ( ','mult':'X','omega':'\omega','pi':'\pi','rightArrow':'\\rightarrow',
       'rightPar':'\\right )','sig':'\sum','smaller':'<','prod':'\prod','sqrt':'\sqrt','Theta':'\Theta',
       'Unequal':'\\neq', 'Union': '\cup', None:None}

      if latexFormat.__contains__(symbol):
        return latexFormat[symbol]

      else:
        return symbol
