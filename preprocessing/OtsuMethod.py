import cv2 as cv

class OtsuMethod(object):
    """
    OtsuMethod used to convert image into binary image.
    """

    def __init__(self):
        super(OtsuMethod, self).__init__()

    def ConvertToBinaryImage(self, imagePath):
        """
        Open the original image, convert it to binary, save the binary image in the sam directory
        of the originak one and return the path to the binary image.
        :param imagePath: path to the image we want to convert into binary image
        :type imagePath: string
        """
        img = cv.imread(imagePath, 0)
        ret, binaryImage = cv.threshold(img, 127, 255, cv.THRESH_BINARY_INV)
        # Add "_bin" to the name of the binary image.
        parts = imagePath.split(".")
        binaryImagePath = parts[0] + "_bin." + parts[1]
        # Save the binary image in the same directory.
        cv.imwrite(binaryImagePath, binaryImage)
        # Return the path to the binary image.
        return binaryImagePath




