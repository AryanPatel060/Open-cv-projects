import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui
import math

wCam ,hCam = 1280 ,720
pTime = 0

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

colorR = 255 , 0 , 255
cX , cY , w , h  = 100 ,100 , 200 ,200


detector  = htm.handDetector()


class DragRect():
    def __init__(self,posCenetr , size=[200,200]):
        self.size = size
        self.posCenter = posCenetr
    def update(self,x1,y1):
          cX ,cY = self.posCenter
          w , h = self . size
          
          if cX - w//2 < x1 < cX + w //2  and cY- h//2 < y1 < cY + h //2:
                self. posCenter  = x1 ,y1
                
                # colorR  = 0 , 255 , 0
                # cX , cY = x1, y1 
rectList = []
for x in range(5):
    rectList.append(DragRect([x*250+150,150]))

        

while True :
    sccess , img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img , draw=False)
    lmlist = detector.findPossition(img)

    if lmlist :
        x1 , y1 = lmlist[8][1:]
        x2,y2 = lmlist[12][1:]
        length = math.hypot(x2-x1 , y2-y1)
        cv2.line(img , (x1,y1), (x2,y2),(0,0,255) , 2)
        if length < 50 :
            for rects in rectList:
                rects.update(x1,y1)
          
        else:
            colorR = 255 , 0 , 255
    imgnew =  np.zeros_like(img, np.uint8)
    for rects in rectList:
        cX ,cY = rects.posCenter
        w , h = rects . size   
        cv2.rectangle(imgnew,(cX - w//2,cY- h//2),(cX + w //2 , cY + h //2),colorR,cv2.FILLED)
    
    out  = img.copy()
    alpha = 0.5
    mask = imgnew.astype(bool)
    out[mask] = cv2.addWeighted(img , alpha , imgnew  ,1 - alpha  , 8 )[mask]       
    
    cTime= time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(out,f'FPS : {int(fps)}',(40,50), cv2.FONT_HERSHEY_COMPLEX, 1,(0,0,255) , 2)
    cv2.imshow("Image",out)
    cv2.waitKey(1)
