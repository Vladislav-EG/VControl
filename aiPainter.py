import cv2
import WorkingHands
import numpy as np


# COLOSRS
BLACK = (0, 0, 0)
RED = (0, 0, 255)
PURPLE = (255, 0, 255)
ORANGE = (0, 100, 255)
BROWN = (5, 85, 160)
YELLOW = (0, 255, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
CYAN = (255, 255, 0)
WHITE = (255, 255, 255)

COLORS = [RED, PURPLE, ORANGE, GREEN, BLUE, CYAN, WHITE, BLACK]
BRUSH_SIZE = [25, 23, 20, 18, 15, 10] 

y1_draw_rec = 0
y2_draw_rec = y1_draw_rec + 100

imgCanvas = np.zeros((720, 1280, 3), np.uint8)

def draw_all(img):
    x1_draw_rec = 128
    x2_draw_rec = x1_draw_rec + 128

    for color in COLORS:
        new_img = cv2.rectangle(img, (x1_draw_rec, y1_draw_rec), (x2_draw_rec, y2_draw_rec), color, cv2.FILLED)
        x1_draw_rec += 128
        x2_draw_rec += 128

    # x_brush = 64
    # for brush in BRUSH_SIZE:
    #     new_img = cv2.circle(img, (x_brush, 50), brush, BLACK, cv2.FILLED) 
    #     x_brush += 158

    # new_img = cv2.rectangle(img, (1000, 15), (1200, 70), (203, 192, 255), cv2.FILLED) 
    return new_img


def color_selection(x1, drawColor):
    if 128 < x1 < 256:
        drawColor = RED
        return drawColor
    elif 256 < x1 < 384:
        drawColor = PURPLE
        return drawColor
    elif 384 < x1 < 512:
        drawColor = ORANGE
        return drawColor
    elif 512 < x1 < 640:
        drawColor = GREEN
        return drawColor
    elif 640 < x1 < 768:
        drawColor = BLUE
        return drawColor
    elif 768 < x1 < 896:
        drawColor = CYAN
        return drawColor
    elif 896 < x1 < 1024:
        drawColor = WHITE
        return drawColor
    elif 1024 < x1 < 1152:
        drawColor = BLACK
        return drawColor


def main(img, drawColor, lmList, fingers, xp, yp):
    new_img = draw_all(img)

    if lmList:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        if fingers == [0, 1, 1, 0, 0]:
            xp, yp = 0, 0
            cv2.rectangle(new_img, (x1, y1 - 15), (x2, y2 + 15), drawColor, cv2.FILLED)
            if y1 < 100:
                drawColor = color_selection(x1, drawColor)
                
        if fingers == [0, 1, 0, 0, 0]:
            cv2.circle(new_img, (x1, y1), 15, drawColor, cv2.FILLED)

            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawColor == (0, 0, 0):
                cv2.line(new_img, (xp, yp), (x1, y1), drawColor, 40)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, 40)
            else:
                cv2.line(new_img, (xp, yp), (x1, y1), drawColor, 15)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, 15)

            xp, yp = x1, y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    new_img = cv2.bitwise_and(new_img, imgInv)
    new_img = cv2.bitwise_or(new_img, imgCanvas)

    # cv2.imshow("img", imgCanvas)

    # new_img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    return new_img, drawColor, xp, yp