
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

      if symbol.startswith('alpha'):
          return '\\alpha'
      elif symbol.startswith('beta'):
          return '\\beta'
      elif symbol.startswith('bigger'):
          return '>'
      elif symbol.startswith('dot'):
          return '\cdot'
      elif symbol.startswith('epsilon'):
          return '\epsilon'
      elif symbol.startswith('fi'):
          return '\phi'
      elif symbol.startswith('frac'):
          return 'frac'
      elif symbol.startswith('gama'):
          return '\gamma'
      elif symbol.startswith('infinity'):
          return '\infty'
      elif symbol.startswith('integral'):
          return '\int'
      elif symbol.startswith('lambda'):
          return '\lambda'
      elif symbol.startswith('leftArrow'):
          return '\leftarrow'
      elif symbol.startswith('leftPar'):
          return '\left ( '
      elif symbol.startswith('mult'):
          return 'X'
      elif symbol.startswith('omega'):
          return '\omega'
      elif symbol.startswith('pi'):
          return '\pi'
      elif symbol.startswith('plus'):
          return '+'
      elif symbol.startswith('rightPar'):
          return '\\right )'
      elif symbol.startswith('sig'):
          return '\sum'
      elif symbol.startswith('smaller'):
          return '<'
      elif symbol.startswith('prod'):
          return '\prod'
      elif symbol.startswith('sqrt'):
          return '\sqrt'
      elif symbol.startswith('teta'):
          return '\Theta'
      elif symbol.startswith('uneqal'):
          return '\\neq'
      elif symbol.startswith('uonin'):
          return '\\bigcap'

temp = ConvertStringToLatexFormat()
res = temp.ConvertToLatexFormat("prod44234")
print (res)