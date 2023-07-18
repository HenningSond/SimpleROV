import cv2, socket, numpy, pickle
from PyQt5.QtWidgets import *
import sys
from GUI_MAIN import MainWindow
import numpy as np
from PyQt5.QtCore import *
import threading
import Values
import pygame
import time
import struct

def RovCamera():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip = "169.254.36.156"
    #ip = "169.254.226.72"
    port = 6666
    s.bind((ip, port))
    while True:
        x=s.recvfrom(1000000)
        clientip = x[1][0]
        data=x[0]

        data=pickle.loads(data)

        data = cv2.imdecode(np.frombuffer(data, dtype=np.uint8),1)
        Values.rovCamera = data
        #print(data)

def JoyStick():
    Ready = True
    pygame.init()
    print(pygame.joystick.get_count())
    if pygame.joystick.get_count() == 1:
        pygame.display.init()
        pygame.joystick.init()
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print(pygame.joystick.get_init())
        while Ready:
            # Get controller readings
            pygame.event.get()

            Values.Joy_X_Val = round(joystick.get_axis(0),3)
            Values.Joy_Y_Val = round(joystick.get_axis(1),3)
            Values.Joy_Z_Val = round(joystick.get_axis(4),3)
            Values.Joy_H_Val = joystick.get_hat(0)
            Values.LightPower = round(joystick.get_axis(2),3)
            print(Values.LightPower)
            if (pygame.joystick.get_count() != 1):
                print("Joystick disconnected")
                break
    else:
        print("No Joystick Available")

def ResiveValues():
    reseve = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip1 = "169.254.36.156"
    port1 = 6668
    reseve.bind((ip1, port1))
    StartTime = time.time()

    try:
        while True:
            Runtime = time.time() - StartTime
            DataInn = reseve.recvfrom(100)
            data = DataInn[0]
            data = pickle.loads(data)
            #print([data, round(Runtime,3)])
    except:
        pass

def SendValues():
    StartTime = time.time()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 100)
    serverip = "169.254.226.72"
    serverport = 6670

    time.sleep(2.0)
    while True:
        Runtime = round((time.time() - StartTime), 3)
        time.sleep(0.01)
        v = [Values.Joy_X_Val, Values.Joy_Y_Val, Values.Joy_Z_Val, Values.Joy_H_Val, Values.LightPower, Runtime]
        x_as_bytes = pickle.dumps(v)
        s.sendto(x_as_bytes, (serverip, serverport))
        #print(Runtime)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = MainWindow()
    cam_communication = threading.Thread(target=RovCamera)
    cam_communication.start()
    Joy_Values = threading.Thread(target=JoyStick)
    Joy_Values.start()
    UdpRes = threading.Thread(target=ResiveValues)
    UdpRes.start()
    UdpSen = threading.Thread(target=SendValues)
    UdpSen.start()
    a.show()
    sys.exit(app.exec_())
