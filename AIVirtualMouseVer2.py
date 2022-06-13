import cv2
import numpy as np
import WorkingHands as wh
import time
import autopy
import math
import pyautogui
import GestureFunction

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import threading

from PyQt6.QtGui import QImage, QPixmap


def main(ui, cap):
    wCam, hCam = 1280, 720 # 600
    frameR = 300 # 230
    smoothing = 13 # 13

    old_combo = "basic"

    pTime = 0
    plocX, plocY = 0, 0 
    clocX, clocY = 0, 0

    #cap = cv2.VideoCapture(0)
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, wCam)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hCam)
    wScr, hScr = autopy.screen.size()

    detector = wh.handDetector(maxHands=2)
    gestureFunc = GestureFunction.CollectionGesture()

    basic_lenght_finger = 50

    en_keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "*"],
            ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "?", "$"],
            [" ", " ", " ", "SH", "LN", "EN", "CL", " ", " ", " ",],]

    ru_keys = [["Й", "Ц", "У", "К", "Е", "Н", "Г", "Ш", "Щ", "З", "Х", "Ъ"],
            ["Ф", "Ы", "В", "А", "П", "Р", "О", "Л", "Д", "Ж", "Э", ";"],
            ["Я", "Ч", "С", "М", "И", "Т", "Ь", "Б", "Ю", ",", ".", "?"],
            [" ", " ", " ", "SH", "LN", "EN", "CL", " ", " ", " ",],]

    keys = ru_keys
    finalText = ""
    register = ""
    drawColor = (0, 0 ,0)
    xp, yp = 0, 0 

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img, draw=False)
        
        if len(lmList) != 0:
            x1, y1 = lmList[12][1:] 

            # cv2.rectangle(img, (frameR, frameR), (wCam-frameR, hCam-frameR), (255, 0, 255), 2)
            
            changeable_lenght_finger = detector.findDistance(11, 12, img, draw=False)[0] # изменить

            fingers = detector.halfFingersUp()

            if fingers == [1, 1, 1, 1, 1]:
                if old_combo == "took":
                    pyautogui.mouseUp(button = "left")
                    # time.sleep(.3)
                
                basic_lenght_finger = gestureFunc.basic(img, detector)
                old_combo = "basic"

            if fingers == [0, 1, 1, 0, 0] and changeable_lenght_finger + 10 > basic_lenght_finger and old_combo != "keyboard_mode" and old_combo != "ai_keyboard" and old_combo != "ai_painter":
                gestureFunc.moveMouse(img, detector, x1, y1)
                old_combo = "move_mouse"

            if fingers == [0, 1, 1, 0, 0] and old_combo == "move_mouse":
                gestureFunc.double_click(img, detector, x1, y1)
                # old_combo = "double_click"

            if fingers == [0, 0, 1, 0, 0] and old_combo == "move_mouse":
                gestureFunc.left_click()
                old_combo = "left_click"   
       
            if fingers == [0, 1, 0, 0, 0] and old_combo == "move_mouse":
                gestureFunc.right_click()
                old_combo = "right_click"

            if fingers == [1, 1, 0, 0, 0] and (old_combo == "basic" or old_combo == "volume_control"):
                gestureFunc.volume_control(img, lmList)
                old_combo = "volume_control"

            if fingers == [0, 0, 0, 0, 0] and old_combo != "keyboard_mode" and old_combo != "ai_painter":
                if old_combo == "basic" or old_combo == "move_mouse":
                    gestureFunc.drag_and_drop()
                    old_combo = "took"
                else:
                    gestureFunc.moveMouse(img, detector, x1, y1)
                    
            if fingers == [0, 1, 1, 1, 1] and (old_combo == "basic" or old_combo == "move_mouse" or old_combo == "hscroll"): 
                gestureFunc.hscroll(img, y1)
                old_combo = "hscroll"

            if fingers == [0, 1, 1, 1, 0] and (old_combo == "basic" or old_combo == "move_mouse" or old_combo == "hscroll"):            
                old_combo = "keyboard_mode" 
            
            if fingers == [1, 0, 0, 0, 0] and old_combo == "keyboard_mode":
                gestureFunc.change_language()

            if fingers == [0, 1, 1, 0, 0] and old_combo == "keyboard_mode":
                my_thread = threading.Thread(target=gestureFunc.voice_input)
                my_thread.start()
                old_combo = "voice_input"
            
            if (fingers == [0, 1, 0, 0, 0] and old_combo == "keyboard_mode") or (old_combo == "ai_keyboard"):
                img, finalText, keys = gestureFunc.ai_keyboard(img, lmList, detector, keys, ru_keys, en_keys, finalText, register)
                old_combo = "ai_keyboard"
                
            if fingers == [0, 1, 0, 0, 1]:
                old_combo = "special"

            if (fingers == [0, 1, 0, 0, 0] and old_combo == "special") or old_combo == "ai_painter":
                img, drawColor, xp, yp = gestureFunc.ai_painter(img, lmList, fingers, drawColor, xp, yp)
                old_combo = "ai_painter"
        
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, str(str(int(fps)) + " - " + old_combo), (5, 40),
                    cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 51, 102), 2)

        # cv2.imshow("Image", img)
        displayImage(img, ui, 1)
        if cv2.waitKey(1) == 27:  
            break

        
def displayImage(img, ui, window = 0):
    qFormat = QImage.Format.Format_RGB888

    img = QImage(img, 1280, 600, qFormat) # img.shape[0], img.shape[1]
    img = img.rgbSwapped()

    ui.img_label.setPixmap(QPixmap.fromImage(img))

