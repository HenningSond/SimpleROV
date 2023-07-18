
import serial
import time
import math
StartTime = time.time()
arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
def write_read(Send_data):
    Runtime = time.time() - StartTime
    sine = round(15 * math.cos(50 * Runtime + 1), 3)
    Send_data[2] = sine

    Send_message = '<e'+str(Send_data[0])+'f'+str(Send_data[1])+'g'+str(Send_data[2])+'h'+str(Send_data[3])+'i>'
    #print(bytes(Send_message, 'utf-8'))
    arduino.write(bytes(Send_message, 'utf-8'))
    time.sleep(0.05)
    rawData = arduino.readline()
    strData = rawData.strip().decode('utf-8').split()
    #print(rawData)
    try:

        for i in range(0, len(strData)):
            strData[i] = float(strData[i])
        return strData

    except:
        pass

while True:
    num = [1.23, 2.34, 3.45, 4.56]
    value = write_read(num)
    print(value) 