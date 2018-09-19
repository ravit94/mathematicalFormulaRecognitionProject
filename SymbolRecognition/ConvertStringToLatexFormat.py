import time 
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
      latexFormat = {'alpha'        : '\\alpha',
                     'beta'         : '\\beta',
                     'bigger'       : '>',
                     'dot'          : '\cdot',
                     'epsilon'      : '\epsilon',
                     'phi'          : '\phi',
                     'frac'         : '\\frac',
                     'gamma'        : '\gamma',
                     'infinity'     : '\infty',
                     'integral'     : '\int_',
                     'lambda'       : '\lambda',
                     'leftArrow'    : '\leftarrow',
                     'leftPar'      : '\left ( ',
                     'mult'         : 'X',
                     'omega'        : '\omega',
                     'pi'           : '\pi ',
                     'rightArrow'   : '\\rightarrow',
                     'rightPar'     : '\\right )',
                     'sig'          : '\sum',
                     'smaller'      : '<',
                     'prod'         : '\prod',
                     'sqrt'         : '\sqrt',
                     'Theta'        : '\Theta',
                     'Unequal'      : '\\neq',
                     'Union'        : '\cup'}

      if symbol == None:
          return None
      if symbol.__contains__("."):
          symbol = symbol.split(".")[0]
          if latexFormat.__contains__(symbol):
            return latexFormat[symbol]
          symbol = symbol[:-1]
          if latexFormat.__contains__(symbol):
            return latexFormat[symbol]
      return symbol

   def CreateLatexFile(self, resultString, outputFilePath):
      """
      This function receive the result string from the recognition in latex format
      and create editable latex file included the option to displayed as pdf file also.
      :param resultString: received by the process of structure analysis.
      :type resultString: string
      :param outputFilePath: path to the output file.
      :type outputFilePath: string
      """
      latexFormat = "\documentclass[12pt]{article}" + "\n\\usepackage{amsmath}"\
                    +"\n\\usepackage{graphicx}"+"\n\\usepackage{hyperref}" \
                    +"\n\\usepackage[latin1]{inputenc}"+"\n" \
                    +"\n\\title{Editable LaTeX file}"+"\n\\date{}".format(time.strftime("%d/%m/%Y")) \
                    +"\n\\begin{document}"+"\n\\maketitle" \
                    +"\nYou convert the image" + outputFilePath + "to \LaTeX{} and now you can edit the file!" \
                    +"\n\\begin{equation}"+"\n\n" + resultString +"\n\n\\end{equation}"+"\n\n\\end{document}"
      path = outputFilePath.split(".")[0]
      path = path + ".tex"
      text_file = open(path, "w+")

      text_file.write(latexFormat)

      text_file.close()
