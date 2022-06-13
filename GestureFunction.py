import cv2
import numpy as np
from win10toast import ToastNotifier
import WorkingHands as wh
import time
import autopy
import math
import pyautogui
import keyboard
import speech_recognition
import win32api
import win32gui
import win32con
import win32com.client

from win10toast import ToastNotifier
from threading import Thread

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import alertForVoice
import getKeyboardLanguage
import webcamKeyboard
import aiPainter



wCam, hCam = 1280, 720 
frameR = 300 
smoothing = 13 
wScr, hScr = autopy.screen.size()

# Переменные для volume_control - контроля звука
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxnVol = volRange[1]
#old_vol = 0


class CollectionGesture():
    def __init__(self, basic_lenght_finger=50, plocX=0, plocY=0, old_vol=0):
        self.basic_lenght_finger = basic_lenght_finger
        self.plocX = plocX
        self.plocY = plocY
        self.old_vol = old_vol
        
    def basic(self, img, detector):
        self.basic_lenght_finger = detector.findDistance(11, 12, img, draw=False)[0] # изменить
        return self.basic_lenght_finger

    def moveMouse(self, img, detector, x1, y1):
        # lenght, img, lineInfo = detector.findDistance(8, 12, img, draw=False) 
        
        x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
        y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))

        clocX = self.plocX + (x3 - self.plocX) / smoothing
        clocY = self.plocY + (y3 - self.plocY) / smoothing

        try:
            autopy.mouse.move(wScr - clocX, clocY)
        except:
            print(1)
        self.plocX, self.plocY = clocX, clocY
        

    def left_click(self):
        autopy.mouse.click()
        # time.sleep(.3)
        return "left_click"

    def right_click(self):
        autopy.mouse.click(autopy.mouse.Button.RIGHT)
        # time.sleep(.3)
        return "right_click"

    def double_click(self, img, detector, x1, y1):
        lenght, img, lineInfo = detector.findDistance(8, 12, img, draw=True)  # изменить  

        if lenght < 55: # изменить
            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)

            autopy.mouse.click()
            autopy.mouse.click()
            # time.sleep(.3)
         
        cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED) 

    def volume_control(self, img, lmList):
        x_thumb, y_thumb = lmList[4][1], lmList[4][2]
        x_forefinger, y_forefinger = lmList[8][1], lmList[8][2]
        cx_vol, cy_vol = (x_thumb + x_forefinger) // 2, (y_thumb + y_forefinger) // 2

        cv2.line(img, (x_thumb, y_thumb), (x_forefinger, y_forefinger), (255, 0, 255), 3)
        cv2.circle(img, (cx_vol, cy_vol), 15, (0, 255, 0), cv2.FILLED)

        lenght_thump_foref = math.hypot(x_forefinger - x_thumb, y_forefinger - y_thumb)

        vol = np.interp(lenght_thump_foref, [50, 280], [minVol, maxnVol])

        if vol > self.old_vol + 0.8 or vol < self.old_vol - 0.8: # проверка на дрожание пальцев
            volume.SetMasterVolumeLevel(vol, None)
        
        self.old_vol = vol

    def drag_and_drop(self):
        pyautogui.mouseDown(button = "left")
        pyautogui.moveTo(pyautogui.position()[0], pyautogui.position()[1], duration = 0.1)
        # time.sleep(.3)

    def hscroll(self, img, y1):
        cv2.rectangle(img, (230, 330), (wCam-230, 330+70), (0, 0, 255), 2)

        if y1 < 330:
            if y1 < 260:
                pyautogui.hscroll(200)
            else:
                pyautogui.hscroll(200)
        elif y1 > 330 + 70:
            if y1 > 390 + 70:
                pyautogui.hscroll(-200)
            else:
                pyautogui.hscroll(-200)

    def voice_input(self):
        sr = speech_recognition.Recognizer()
        query = ""
        #sr.pause_threshold = 0.5
        alertForVoice.main()
        keyboard_language = getKeyboardLanguage.get_keyboard_language()

        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic)
            if keyboard_language == "Russian":
                try:
                    query = sr.recognize_google(audio_data=audio, language="ru-Ru").lower() 
                except speech_recognition.UnknownValueError:
                    print("Невозможно распознать речь/Тишина")                                  
            elif keyboard_language == "English - United States":
                try:
                    query = sr.recognize_google(audio_data=audio, language="en-En").lower()
                except speech_recognition.UnknownValueError:
                    print("Невозможно распознать речь/Тишина")  

            # if query.split()[0] == "английский":
            #     query = sr.recognize_google(audio_data=audio, language="en-En").lower()
            #     query = " ".join(query.split()[1:]) 
        if len(query) > 0:
            keyboard.write(query)
        # pyautogui.press('enter') 

    def change_language(self):
        pyautogui.hotkey("shift", 'alt')
        # time.sleep(0.4)
    
    def ai_keyboard(self, img, lmList, detector, keys, ru_keys, en_keys, finalText, register):
        new_img, finalText, keys = webcamKeyboard.main(img, lmList, detector, keys, ru_keys, en_keys, finalText, register)
        return new_img, finalText, keys  

    def ai_painter(self, img, lmList, fingers, drawColor, xp, yp):
        new_img, drawColor, xp, yp = aiPainter.main(img, drawColor, lmList, fingers, xp, yp)

        hwnd = win32gui.FindWindow(None, "MainWindow") # Название приложения 
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(hwnd)
        return new_img, drawColor, xp, yp