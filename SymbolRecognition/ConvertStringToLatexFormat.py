
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
      if symbol == None:
          return None
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
      elif symbol.startswith('phi'):
          return '\phi'
      elif symbol.startswith('frac'):
          return '\\frac'
      elif symbol.startswith('gamma'):
          return '\gamma'
      elif symbol.startswith('infinity'):
          return '\infty'
      elif symbol.startswith('integral'):
          return '\int_'
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
      elif symbol.startswith('rightArrow'):
          return '\\rightarrow'
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
      elif symbol.startswith('Theta'):
          return '\Theta'
      elif symbol.startswith('Unequal'):
          return '\\neq'
      elif symbol.startswith('Union'):
          return '\cup'
      else:
          return symbol