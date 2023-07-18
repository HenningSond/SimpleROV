import sys

import numpy as np
from PyQt5.QtGui import *
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import Values
import cv2
import pygame
import socket
import pickle
import struct ## new

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        #-------------------------------------- Main Window

        self.setWindowTitle("ROV")
        self.setGeometry(0,0,1920,1080)

        #self.setStyleSheet("background-color: rgb(93, 93, 93);")

        #--------------------------------------- ROV camera window

        self.image_label = QLabel(self)
        self.image_label.setGeometry(20, 50, 1300, 780)
        self.image_label.setFrameShape(QFrame.Panel)

        #--------------------------------------- action logger

        self.log_lable = QLabel(self)
        self.log_lable.setGeometry(1350, 50 ,500 ,500)
        self.log_lable.setFrameShape(QFrame.Panel)





        #----------------------------------------Clock
        self.Clock = QLabel(self)
        self.Clock.setGeometry(1830,10,70,25)
        self.Clock.setFrameShape(QFrame.Panel)
        timer = QTimer(self)
        timer.timeout.connect(self.Update_Clock)
        timer.start(1000)
        #---------------------------------------------------------

        self.Forward = QCheckBox(self)
        self.Forward.setGeometry(QRect(110, 10, 25, 25))
        self.Forward.setIconSize(QSize(40, 40))

        self.IP_set =QLineEdit(self)
        self.IP_set.setGeometry(20,10,80,25)

        self.Worker1 =VideoUpdate()
        self.Worker1.Vidoe_signal.connect(self.Update_image)
        self.Worker1.start()

    def Update_Clock(self):
        current_time = QTime.currentTime()
        # converting QTime object to string
        label_time = current_time.toString('hh:mm:ss')
        self.Clock.setText(label_time)

    def Update_image(self, cv_img):
        qt_img = self.convert_video_qt(cv_img)
        self.image_label.setPixmap(qt_img)


    def convert_video_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(1920, 1080, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)



class VideoUpdate(QThread):
    Vidoe_signal = pyqtSignal(np.ndarray)
    def __init__(self):
        super().__init__()
        self._run_flag = True
    def run(self):
        while self._run_flag:
            try:
                if (len(Values.rovCamera) > 10):
                    self.Vidoe_signal.emit(Values.rovCamera)
                    Values.rovCamera = np.array([])
            except:
                continue
    def stop(self):
        self._run_flag = False
        self.wait()
