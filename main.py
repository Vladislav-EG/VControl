from venv import create
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from PyQt6 import uic
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QImage, QPixmap, QMovie 
from PyQt6 import QtCore
from PyQt6.QtCore import QPropertyAnimation
from PySide2 import QtWidgets
from qt_material import apply_stylesheet

from goodGui import Ui_MainWindow

import os, sys
import cv2
import numpy as np
import threading

import AIVirtualMouseVer2


wCam, hCam = 1280, 600 


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.webcam_btn.clicked.connect(self.show_webcam_page)
        self.ui.instruction_btn.clicked.connect(self.show_instruction_page)
        self.ui.about_btn.clicked.connect(self.show_about_page)
        self.ui.pushButton.clicked.connect(self.slideLeftMenu)

        self.ui.stackedWidget.setCurrentWidget(self.ui.about_page)
        
        self.cap = cv2.VideoCapture(0)
        self.show()

    def closeEvent(self, event):
        self.cap.release()
        cv2.destroyAllWindows()
 
    def show_webcam_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.webcam_page)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, wCam)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hCam)

        AIVirtualMouseVer2.main(self.ui, self.cap)

        self.cap.release()
        cv2.destroyAllWindows()

    def show_instruction_page(self):            
        self.ui.stackedWidget.setCurrentWidget(self.ui.instruction_page)

        self.createGif()

    def show_about_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.about_page)
        
    def displayImage(self, img, window = 0):
        qFormat = QImage.Format.Format_RGB888

        img = QImage(img, 1280, 600, qFormat) # img.shape[0], img.shape[1]
        img = img.rgbSwapped()

        self.ui.img_label.setPixmap(QPixmap.fromImage(img))
    
    def slideLeftMenu(self):
        width = self.ui.left_menu_cont_frame.width()

        if width == 60:
            new_width = 160
        else:
            new_width = 60

        self.animation = QPropertyAnimation(self.ui.left_menu_cont_frame, b'minimumWidth')
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuad)
        self.animation.start()

    def cleanUp(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def createGif(self):
        self.anim = QMovie(r"C:\Users\vlade\OneDrive\Рабочий стол\DIPLOM\goodVersion27.03.2022\testVerSAVE3\DIPLOM_GIF\base.gif")
        self.ui.label_8.setMovie(self.anim)
        self.anim.start()

        self.anim = QMovie(r"C:\Users\vlade\OneDrive\Рабочий стол\DIPLOM\goodVersion27.03.2022\testVerSAVE3\DIPLOM_GIF\move_mouse.gif")
        self.ui.label_12.setMovie(self.anim)
        self.anim.start()

        self.anim = QMovie(r"C:\Users\vlade\OneDrive\Рабочий стол\DIPLOM\goodVersion27.03.2022\testVerSAVE3\DIPLOM_GIF\left_click.gif")
        self.ui.label_16.setMovie(self.anim)
        self.anim.start()

        self.anim = QMovie(r"C:\Users\vlade\OneDrive\Рабочий стол\DIPLOM\goodVersion27.03.2022\testVerSAVE3\DIPLOM_GIF\right_click.gif")
        self.ui.label_22.setMovie(self.anim)
        self.anim.start()

        self.anim = QMovie(r"C:\Users\vlade\OneDrive\Рабочий стол\DIPLOM\goodVersion27.03.2022\testVerSAVE3\DIPLOM_GIF\double_click.gif")
        self.ui.label_20.setMovie(self.anim)
        self.anim.start()

        self.anim = QMovie(r"C:\Users\vlade\OneDrive\Рабочий стол\DIPLOM\goodVersion27.03.2022\testVerSAVE3\DIPLOM_GIF\volume_control.gif")
        self.ui.label_18.setMovie(self.anim)
        self.anim.start()

        self.anim = QMovie(r"C:\Users\vlade\OneDrive\Рабочий стол\DIPLOM\goodVersion27.03.2022\testVerSAVE3\DIPLOM_GIF\took.gif")
        self.ui.label_10.setMovie(self.anim)
        self.anim.start()

        self.anim = QMovie(r"C:\Users\vlade\OneDrive\Рабочий стол\DIPLOM\goodVersion27.03.2022\testVerSAVE3\DIPLOM_GIF\hscroll.gif")
        self.ui.label_24.setMovie(self.anim)
        self.anim.start()

        self.anim = QMovie(r"C:\Users\vlade\OneDrive\Рабочий стол\DIPLOM\goodVersion27.03.2022\testVerSAVE3\DIPLOM_GIF\keyboard_mode.gif")
        self.ui.label_14.setMovie(self.anim)
        self.anim.start()

        self.anim = QMovie(r"C:\Users\vlade\OneDrive\Рабочий стол\DIPLOM\goodVersion27.03.2022\testVerSAVE3\DIPLOM_GIF\change_ln.gif")
        self.ui.label_26.setMovie(self.anim)
        self.anim.start()

        self.anim = QMovie(r"C:\Users\vlade\OneDrive\Рабочий стол\DIPLOM\goodVersion27.03.2022\testVerSAVE3\DIPLOM_GIF\ai_keyboard.gif")
        self.ui.label_36.setMovie(self.anim)
        self.anim.start()

        self.anim = QMovie(r"C:\Users\vlade\OneDrive\Рабочий стол\DIPLOM\goodVersion27.03.2022\testVerSAVE3\DIPLOM_GIF\voice_input.gif")
        self.ui.label_34.setMovie(self.anim)
        self.anim.start()

        self.anim = QMovie(r"C:\Users\vlade\OneDrive\Рабочий стол\DIPLOM\goodVersion27.03.2022\testVerSAVE3\DIPLOM_GIF\special_mode.gif")
        self.ui.label_32.setMovie(self.anim)
        self.anim.start()

        self.anim = QMovie(r"C:\Users\vlade\OneDrive\Рабочий стол\DIPLOM\goodVersion27.03.2022\testVerSAVE3\DIPLOM_GIF\ai_painter.gif")
        self.ui.label_30.setMovie(self.anim)
        self.anim.start()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    
    main_win.show()
    sys.exit(app.exec())