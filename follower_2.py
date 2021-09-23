import cv2
import numpy as np


def get_mask(frame):
    # blur image to reduse noise '
    blured_img = cv2.GaussianBlur(frame, (5, 5), 1)
    # convert to gray
    gray = cv2.cvtColor(blured_img, cv2.COLOR_BGR2GRAY)
    # threthold the image
    ret, img_bin = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # reverse the binary image to get the mask needed
    img_bin = 255 - img_bin
    # A kernel of (10 X 10) ones.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    kernel_1 = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    # apply erosion & dilation to get rid of the noise
    img_bin = cv2.dilate(img_bin, kernel_1, 10)

    img_bin = cv2.erode(img_bin, kernel, 10)

    return img_bin


def find_dir(mask, xsetpoint, ysetpoint):
    global x_last, y_last

    contours, herarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours_len = len(contours)

    if contours_len > 0:
        con = max(contours, key=cv2.contourArea)
        blackbox = cv2.minAreaRect(con)

        (x_min, y_min), (w_min, h_min), ang = blackbox
        x_last = x_min
        y_last = y_min
        if ang < -45:
            ang = 90 + ang
        if w_min < h_min and ang > 0:
            ang = (90 - ang) * -1
        if w_min > h_min and ang < 0:
            ang = 90 + ang

        ang = int(ang)
        if abs(ang) < 65:
            error = int(x_min - xsetpoint)
        else:
            error = int(y_min - ysetpoint)

        box = cv2.boxPoints(blackbox)
        box = np.int0(box)

        return (w_min, h_min, error, ang, box)
    else:
        return (0, 0, 0, 0, None)




def filter_con(con):
    if con is None:
        return 0
    else:
        return cv2.contourArea(con)


def ang_control(error, ang, cbox, rbox, lbox, upbox, downbox):
    global move, direction
    rbox, lbox, upbox, downbox = tuple(map(filter_con, (rbox, lbox, upbox, downbox)))
    turns = [(rbox, 'r'), (lbox, 'l')]
    updown = [(upbox, 'u'), (downbox, 'd')]
    turns = sorted(turns)
    movement = [(rbox, 'r'), (lbox, 'l'), (upbox, 'u'), (downbox, 'd')]
    movement = sorted(movement)

    if not move:
        move = True
        direction = movement[-1][1]
        return direction, 0

    elif move:
        if direction == 'u':
            if ang > 75:
                direction = 'r'
            elif ang < -75:
                direction = 'l'
            elif error > 30:
                error = 'l'
            elif error < -30:
                error = 'r'


        elif direction == 'd':
            if ang > 75:
                direction = 'l'
            elif ang < -75:
                direction = 'r'
            elif error > 30:
                error = 'l'
            elif error < -30:
                error = 'r'

        elif direction == 'r':
            if ang > 75:
                direction = 'u'
            elif ang < -75:
                direction = 'd'
            elif error > 30:
                error = 'd'
            elif error < -30:
                error = 'u'


        elif direction == 'l':
            if ang > 75:
                direction = 'd'
            elif ang < -75:
                direction = 'u'
            elif error > 30:
                error = 'd'
            elif error < -30:
                error = 'u'

        return direction, error


cv2.namedWindow('red mask', cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow('orginal', cv2.WINDOW_GUI_NORMAL)

url = 'http://192.168.43.1:8080/video'

cap = cv2.VideoCapture(url)

x_last = 750

y_last = 600

blist = []
move = False ; direction='';start = False

while True:
    key = cv2.waitKey(1) & 0xFF
    ret, frame= cap.read()
    yf, xf, ch = frame.shape
    mask = get_mask(frame)


    cframe = mask[361:720, 641:1280]
    upframe = mask[0:361, 640:1280]
    dwframe = mask[720:1080, 640:1280]
    rframe = mask[361:720, 1281:1920]
    lframe = mask[361:720, 0:640]

    if key == ord('s'):
        start = not (start)
        move = False
        direction = ''
    if start:
        wc, hc, error, ang, cbox = find_dir(mask, xf // 2, yf // 2)
        _, _, _, _, rbox = find_dir(rframe, xf // 2, yf // 2)
        _, _, _, _, lbox = find_dir(lframe, xf // 2, yf // 2)
        _, _, _, _, upbox = find_dir(upframe, xf // 2, yf // 2)
        _, _, _, _, dwbox = find_dir(dwframe, xf // 2, yf // 2)

        if cbox is not None:
            direction, error = control(error, ang, cbox, rbox, lbox, upbox, dwbox)

            cv2.drawContours(frame, [cbox], 0, (0, 0, 255), 9)
            cv2.putText(frame, str(direction), (cframe.shape[1] // 2, cframe.shape[0] // 2), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 6)
            cv2.putText(frame, str(ang), (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 6)
            # cv2.putText(cframe,str(error),(30, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 6)
            if type(error) is str:
                cv2.putText(frame, str(error), (30, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 6)


    cv2.imshow('red mask', mask)
    cv2.imshow('orginal', frame)


    if key == ord("q"):
        break

cap.release()

cv2.destroyAllWindows()


