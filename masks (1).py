import cv2 as cv
def backp_mask(patren, img):
    #this function take ptren to image and extract semilar one from images
    #I use this fuction to extract one element from image by calculte the probablity of points
    #doc link :  https://docs.opencv.org/4.0.1/dc/df6/tutorial_py_histogram_backprojection.html
    roi = patren
    hsv = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
    target = img

    hsvt = cv.cvtColor(target, cv.COLOR_BGR2HSV)
    # calculating object histogram
    roihist = cv.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
    # normalize histogram and apply backprojection
    cv.normalize(roihist, roihist, 0, 255, cv.NORM_MINMAX)
    dst = cv.calcBackProject([hsvt], [0, 1], roihist, [0, 180, 0, 256], 1)
    # Now convolute with circular disc
    disc = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    cv.filter2D(dst, -1, disc, dst)
    # threshold and binary AND
    ret, thresh = cv.threshold(dst, 50, 255, 0)
    thresh = cv.merge((thresh, thresh, thresh))
    res = cv.bitwise_and(target,thresh)

    return thresh, res

def his_equ_mask(img):
    #this function apply two opencv algorithms adaptive hist equalization & OTSU thresholding
    #resourses : https://pdfs.semanticscholar.org/a4ae/aaf9ba233a3e37d1d04f15207dd413b49c16.pdf
    #https://docs.opencv.org/4.0.1/d5/daf/tutorial_py_histogram_equalization.html

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blured_img = cv.GaussianBlur(gray)

    #adaptive hist equalization
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl1 = clahe.apply(blured_img)

    ret, th = cv.threshold(cl1, 0, 255, cv.THRESH_OTSU)

    return th,cl1


def binary_mask(frame):
    #gat binary mask bu thresholding
    # blur image to reduse noise '
    blured_img = cv.GaussianBlur(frame, (5, 5), 1)
    # convert to gray
    gray = cv.cvtColor(blured_img, cv.COLOR_BGR2GRAY)
    # threthold the image
    ret, img_bin = cv.threshold(gray, 120, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    # reverse the binary image to get the mask needed
    img_bin = 255 - img_bin
    # A kernel of (15 X 15) ones.
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (15, 15))
    kernel_1 = cv.getStructuringElement(cv.MORPH_RECT, (15, 15))
    # apply erosion & dilation to get rid of the noise
    img_bin = cv.erode(img_bin, kernel, 10)
    img_bin = cv.dilate(img_bin, kernel_1, 10)

    return img_bin
