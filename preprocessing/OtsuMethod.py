import cv2 as cv
import os
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

        ## (3) minAreaRect on the nozeros
        pts = cv.findNonZero(binaryImage)
        ret = cv.minAreaRect(pts)
        (cx, cy), (w, h), ang = ret
        if w > h:
            w, h = h, w
            ang += 90
        M = cv.getRotationMatrix2D((cx, cy), 0, 1.0)
        rotated = cv.warpAffine(binaryImage, M, (img.shape[1], img.shape[0]))
        hist = cv.reduce(rotated, 1, cv.REDUCE_AVG).reshape(-1)

        th = 2
        H, W = img.shape[:2]
        uppers = [y for y in range(H - 1) if hist[y] <= th and hist[y + 1] > th]
        lowers = [y for y in range(H - 1) if hist[y] > th and hist[y + 1] <= th]

        rotated = cv.cvtColor(rotated, cv.COLOR_GRAY2BGR)
        for y in uppers:
            cv.line(rotated, (0, y), (W, y), (255, 0, 0), 1)

        for y in lowers:
            cv.line(rotated, (0, y), (W, y), (0, 255, 0), 1)

        cv.imwrite("result.png", rotated)
        # Add "_bin" to the name of the binary image.
        parts = imagePath.split(".")
        binaryImagePath = parts[0] + "_bin." + parts[1]
        # Save the binary image in the same directory.
        cv.imwrite(binaryImagePath, binaryImage)
        image = cv.imread(binaryImagePath)
        for i in range(uppers.__len__()):
            file_path = "C:/rows/" + str(i) + '.png'
            directory = os.path.dirname(file_path)
            try:
                os.stat(directory)
            except:
                os.mkdir(directory)
            y = uppers[i] - 20
            x = 0
            h = (lowers[i] - uppers[i]) + 40
            letter = image[y:y + h, x:x + W]
            cv.imwrite(file_path, letter)
        # Return the path to the directory of binary images.
        return directory




