import time
import serial
import cv2
import time
import HandTrackingModule as htm
cap = cv2.VideoCapture(0)
detector  = htm.handDetector()
arduino_port = 'COM4'
baud_rate = 9600
# 115200 is serial number which we set in arduino
# com4 is where arduino connected to your pc
arduino = serial.Serial()
arduino.port = arduino_port
arduino.baudrate = baud_rate
arduino.timeout = 1
arduino.open()
cmd = ''
time.sleep(2)
try:
    while True:
        success ,img = cap.read()
        img = detector.findHands(img , draw=False)
        lmlist = detector.findPossition(img)
        if lmlist:
            print(lmlist)
            cmd = 'ON'
        else:
            cmd = 'OFF'
        cv2.imshow("Image",img)
        cv2.waitKey(1)
        cmd=cmd+'\r'
        arduino.write(cmd.encode())
except KeyboardInterrupt:
    print("KeyboardInterrupt: Stopping the communication.")

finally:
    arduino.close()


