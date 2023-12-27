import time
import serial
import cv2
import time
import HandTrackingModule as htm


tipIds =  [4,8,12,16,20]
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
while True:
        success ,img = cap.read()
        img = detector.findHands(img , draw=False)
        lmlist = detector.findPossition(img)
        # 1. Find landmark 
        # 2. Get the tip of the index fingers
        if len(lmlist)!=0 :
            x1,y1 = lmlist[8][1:]
            x2,y2 = lmlist[12][1:]
            # cv2.circle(img,(x1,y1) , 15 ,(0,0,255) , cv2.FILLED)
            # cv2.circle(img,(x2,y2) , 15 ,(0,0,255) , cv2.FILLED)

        # 3. check which finger is up
            fingers  =[]
            if lmlist[tipIds[0]][1]>lmlist[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1,5):
                if lmlist[tipIds[id]][2]< lmlist[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            fingers = [str(i) for i in fingers]
            cmd = ''.join(fingers)
        cv2.imshow("Image",img)
        cv2.waitKey(1)
        cmd=cmd+'\r'
        print(cmd)
        arduino.write(cmd.encode())
arduino.close()


