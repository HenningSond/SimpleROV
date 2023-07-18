import threading

import cv2
import socket
import pickle

import serial
import time
import math
import Config
StartTime = time.time()


def RovCameaSend():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000)
    serverip = "169.254.36.156"
    serverport = 6666

    cap = cv2.VideoCapture(0)
    cap.set(3, 1920)
    cap.set(4, 1080)
    time.sleep(2.0)
    while True:
        ret, photo = cap.read()

        #cv2.imshow('streaming', photo)

        ret, buffer = cv2.imencode(".jpg", photo, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
        x_as_bytes = pickle.dumps(buffer)

        s.sendto(x_as_bytes, (serverip, serverport))
        if cv2.waitKey(10) == 13:
            break
    cv2.destroyAllWindows()
    cap.release()

def write_read():
    arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)
    while True:

        Runtime = time.time() - StartTime

        try:
            Send_message = '<e'+str(Config.Joy_X_Val)+'f'+str(Config.Joy_Y_Val)+'g'+str(Config.Joy_Z_Val)+'h'+str(Config.Joy_H_Val[0])+'i'+str(Config.Joy_H_Val[1])+\
                           'j'+str(Config.LightPower)+'k>'

            arduino.write(bytes(Send_message, 'utf-8'))
        except:
            pass
        time.sleep(0.05)
        rawData = arduino.readline()
        strData = rawData.strip().decode('utf-8').split()
        try:
            for i in range(0, len(strData)):
                strData[i] = float(strData[i])
            Config.TempSensor = strData[0]
            Config.WaterLeakage = strData[1]
            Config.PressureSensor = strData[2]
            print(strData)
        except:
            pass

def PrintValues():
    while True:
        v1 = Config.PressureSensor
        Runtime = time.time() - StartTime
        sine = round(15 * math.cos(2 * math.pi * 2 * Runtime), 3)
        v = str(sine) + ',' + str(v1) + ',' + str(round(Runtime,4))
        #print(type(v))
        #print(str(v[0])+)
        with open('Data5.txt', 'a') as f:
            f.writelines(v)
            f.writelines('\n')

def SendValues():
    StartTime = time.time()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 100)
    serverip = "169.254.36.156"
    serverport = 6668

    time.sleep(2.0)
    while True:
        Runtime = round((time.time() - StartTime),3)
        time.sleep(0.01)
        v = [Config.PressureSensor, Config.TempSensor, Config.WaterLeakage, Runtime]
        x_as_bytes = pickle.dumps(v)
        s.sendto(x_as_bytes, (serverip, serverport))
        #print(Runtime)

def ResiveValues():
    reseve = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip1 = "169.254.226.72"
    port1 = 6670
    reseve.bind((ip1, port1))
    StartTime = time.time()

    try:
        while True:
            Runtime = time.time() - StartTime
            DataInn = reseve.recvfrom(100)
            data = DataInn[0]
            data = pickle.loads(data)
            Config.Joy_X_Val = data[0]
            Config.Joy_Y_Val = data[1]
            Config.Joy_Z_Val = data[2]
            Config.Joy_H_Val = data[3]
            Config.LightPower = data[4]
            #print([data[4], round(Runtime, 3)])
    except:
        pass

if __name__ == "__main__":
    VideoSend = threading.Thread(target=RovCameaSend)
    VideoSend.start()
    SerialCommunication = threading.Thread(target=write_read)
    SerialCommunication.start()
    ConfigPrint = threading.Thread(target = PrintValues)
    #ConfigPrint.start()
    UDPSendValues = threading.Thread(target=SendValues)
    UDPSendValues.start()
    UdpRes = threading.Thread(target=ResiveValues)
    UdpRes.start()