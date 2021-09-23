import cv2 as cv
import numpy as np
from scipy import stats



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

    return thresh , res


def his_equ_mask(img):
    #this function apply two opencv algorithms adaptive hist equalization & OTSU thresholding
    #resourses : https://pdfs.semanticscholar.org/a4ae/aaf9ba233a3e37d1d04f15207dd413b49c16.pdf
    #https://docs.opencv.org/4.0.1/d5/daf/tutorial_py_histogram_equalization.html

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blured_img = cv.GaussianBlur(gray)

    # adaptive hist equalization
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
    img_bin = cv.dilate(img_bin, kernel_1, 10)

    img_bin = cv.erode(img_bin, kernel, 10)

    return img_bin


def find_vertical_lines_SI(img):
    #this function used to get vertical lines as reference .
    #it returns value  (slope & interception of lines)  we passing throw make_coordinates() to get first and last point of the line

    # covert to gray
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # threshold the image to find shapes
    ret, img_bin = cv.threshold(gray, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    # reverse the binary image to get the mask needed
    img_bin = 255 - img_bin
    # Defining a kernel length
    kernel_length = np.array(img).shape[1] // 100

    # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, kernel_length))

    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    hori_kernel = cv.getStructuringElement(cv.MORPH_RECT, (kernel_length, 1))

    # A kernel of (3 X 3) ones.
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (10, 10))

    # Morphological operation to detect vertical lines from an image
    img_temp1 = cv.erode(img_bin, verticle_kernel, iterations=1)
    verticle_lines_img = cv.dilate(img_temp1, verticle_kernel, iterations=1)

    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv.erode(img_bin, hori_kernel, iterations=1)
    horizontal_lines_img = cv.dilate(img_temp2, hori_kernel, iterations=1)

    # get only the grid ines

    final_img = cv.bitwise_xor(horizontal_lines_img, verticle_lines_img)

    # rduse noise
    kernel_d = cv.getStructuringElement(cv.MORPH_RECT, (7, 7))
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    final_img = cv.bitwise_xor(horizontal_lines_img, verticle_lines_img)
    final_img = cv.erode(final_img, kernel, 1)
    final_img = cv.dilate(final_img, kernel_d, 15)
    final_img = cv.dilate(final_img, kernel_d, 20)
    final_img = cv.erode(final_img, kernel, 3)

    final_img = cv.bitwise_and(final_img, cv.dilate(verticle_lines_img, kernel_d, 15))

    lines = []

    # finding the lines
    lines = cv.HoughLinesP(final_img, 3, np.pi / 180, 100, minLineLength=100, maxLineGap=150)

    lift_fit_x = []
    lift_fit_y = []

    right_fit_x = []
    right_fit_y = []

    lift_fit_av = []
    right_fit_av = []

    for line in lines:
        x1, y1, x2, y2 = line[0]

        if x1 < 500:
            lift_fit_x.append(x1)
            lift_fit_x.append(x2)
            lift_fit_y.append(y1)
            lift_fit_y.append(y2)

        else:
            right_fit_x.append(x1)
            right_fit_x.append(x2)
            right_fit_y.append(y1)
            right_fit_y.append(y2)

    # find the lines by slope & intercept
    if not (len(lift_fit_x) == 0 or len(lift_fit_y) == 0):
        slope, intercept, r_value, p_value, std_err = stats.linregress(lift_fit_x, lift_fit_y)
        lift_fit_av = [slope, intercept]

    if not ((len(right_fit_x) == 0) or (len(right_fit_y) == 0)):
        slope1, intercept1, r_value, p_value, std_err = stats.linregress(right_fit_x, right_fit_y)
        right_fit_av = [slope1, intercept1]
    if not (len(lift_fit_av) == 0 or len(right_fit_av) == 0):

        return (lift_fit_av, right_fit_av)
    else:
        return ([0.00001, 0], [0.000001, 0])



def mak_coordinates(img, param):
    #this function simply take slope and interception point o
    slope = param[0];
    intercept = param[1]
    y1 = img.shape[0]
    y2 = int(y1 * 0.01)
    x1 = int((y1 - intercept) / (slope))
    x2 = int((y2 - intercept) / (slope))
    return ((x1, y1), (x2, y2))


def average_lines(img, minLineLength=100, maxLineGap=150, setpoint=500, hori=False):
    ''' this function take filterd image after erosion & dilation
    and return slope and interception of lines
    hori param if True make that for horizontal lines

    '''

    lines = []

    # finding the lines
    lines = cv.HoughLinesP(img, 3, np.pi / 180, 100, minLineLength=minLineLength, maxLineGap=maxLineGap)

    lift_fit_x = []
    lift_fit_y = []

    right_fit_x = []
    right_fit_y = []

    lift_fit_av = []
    right_fit_av = []

    for line in lines:
        x1, y1, x2, y2 = line[0]

        if hori:
            if y1 < setpoint:
                lift_fit_x.append(x1)
                lift_fit_x.append(x2)
                lift_fit_y.append(y1)
                lift_fit_y.append(y2)

            else:
                right_fit_x.append(x1)
                right_fit_x.append(x2)
                right_fit_y.append(y1)
                right_fit_y.append(y2)

        if x1 < setpoint:
            lift_fit_x.append(x1)
            lift_fit_x.append(x2)
            lift_fit_y.append(y1)
            lift_fit_y.append(y2)

        else:
            right_fit_x.append(x1)
            right_fit_x.append(x2)
            right_fit_y.append(y1)
            right_fit_y.append(y2)

    # find the lines by slope & intercept
    if not (len(lift_fit_x) == 0 or len(lift_fit_y) == 0):
        slope, intercept, r_value, p_value, std_err = stats.linregress(lift_fit_x, lift_fit_y)
        lift_fit_av = [slope, intercept]

    if not ((len(right_fit_x) == 0) or (len(right_fit_y) == 0)):
        slope1, intercept1, r_value, p_value, std_err = stats.linregress(right_fit_x, right_fit_y)
        right_fit_av = [slope1, intercept1]
    if not (len(lift_fit_av) == 0 or len(right_fit_av) == 0):
        return (lift_fit_av, right_fit_av)
    else:
        return ([0.00001, 0], [0.000001, 0])


def vertHori_lines_mask(img):

    ''' this function take the image and extract vertical lines and horizontal lines
    which we could get rid of some of them '''


    # Convert image to gray scale

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # threthold the image
    ret, img_bin = cv.threshold(gray, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    # reverse the binary image to get the mask needed
    img_bin = 255 - img_bin

    # Defining a kernel length
    kernel_length = np.array(img).shape[1] // 100

    # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, kernel_length))

    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    hori_kernel = cv.getStructuringElement(cv.MORPH_RECT, (kernel_length, 1))

    # A kernel of (3 X 3) ones.
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (10, 10))

    # Morphological operation to detect vertical lines from an image
    img_temp1 = cv.erode(img_bin, verticle_kernel, iterations=1)
    verticle_lines_img = cv.dilate(img_temp1, verticle_kernel, iterations=1)

    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv.erode(img_bin, hori_kernel, iterations=1)
    horizontal_lines_img = cv.dilate(img_temp2, hori_kernel, iterations=1)

    return (verticle_lines_img, horizontal_lines_img)


def hsv_mask (img, lower_range =(0,0,0), higher_range=(50,50,50), low_thresh_value = 120, higher_thresh_value=255, thresh_type = cv.THRESH_BINARY+cv.THRESH_OTSU):
    kernel = np.ones((7,7),np.uint8)
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv,lower_range,higher_range)
    closing_mask= cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
    ret,mask = cv.threshold(closing_mask , low_thresh_value,higher_thresh_value,thresh_type)
    res = cv.bitwise_and(img,img, mask= mask)
    return res,mask


def autoCanny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv.Canny(image, lower, upper)

    # return the edged image
    return edged


def isolateColor(img, lower, upper):
    # gust effective hsv mask

    """
    :param img: Image to isolate teh color of
    :param lower: [lowerHue, lowerSat, lowerVal]
    :param upper: [upperHue, upperSat, upperVal]
    :return: Isolated image
    """

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    if lower[0] > upper[0]:
        # If the HSV values wrap around, then intelligently mask it

        upper1 = [180, upper[1], upper[2]]
        mask1  = cv.inRange(hsv, np.array(lower), np.array(upper1))

        lower2 = [0, lower[1], lower[2]]
        mask2  = cv.inRange(hsv, np.array(lower2), np.array(upper))

        mask = mask1 + mask2

    else:
        mask  = cv.inRange(hsv, np.array(lower), np.array(upper))


    final = cv.bitwise_and(img, img, mask=mask)
    return final