import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math 
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam , hCam = 640 ,480
cTime = 0
pTime = 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector()


# from pycaw for volume control of computer 

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volper  = 0
# /////////////////////////////////////////////

while True:
    success , img = cap.read()

    img  = detector.findHands(img)
    lmlist  = detector.findPossition(img ,draw=False)

    if len(lmlist)!=0 :
        x1, y1 = lmlist[4][1],lmlist[4][2]
        x2, y2 = lmlist[8][1],lmlist[8][2]
        cx ,cy = (x1+x2)//2 , (y1+y2)//2
        cv2.circle(img,(x1,y1) , 15 ,(255,0,255) , cv2.FILLED)
        cv2.circle(img,(x2,y2) , 15 ,(255,0,255) , cv2.FILLED)
        cv2.line(img , (x1,y1), (x2,y2),(255,0,255) , 2)
        cv2.circle(img,(cx,cy), 15 ,(255,0,255), cv2.FILLED)

        length = math.hypot(x2-x1 , y2-y1)

        # hand ranage  = 50 - 30 ( as here we take aproximate)
        # Volume range  = -65 - 0 ( from pycaw we get it )

        vol  = np.interp(length, [ 20 ,200 ] , [minVol , maxVol])
        volBar  = np.interp(length, [ 20 ,200 ] , [400 , 150])
        volPer  = np.interp(length, [ 20 ,200 ] , [0 , 100])

        print(length , vol ,minVol , maxVol)
        volume.SetMasterVolumeLevel(vol, None)

        if length<50 :
            cv2.circle(img,(cx,cy), 15 ,(0,255,0), cv2.FILLED)

        cv2.rectangle(img , (50,150) , (85 , 400 ) , (0,0,255) , 2)
        cv2.rectangle(img , (50,int(volBar)) , (85 , 400 ) , (0,0,255) , cv2.FILLED)
        cv2.putText(img,f'{int(volPer)}%',(40,450), cv2.FONT_HERSHEY_COMPLEX, 1,(0,0,255) , 2)


    cTime= time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,f'FPS : {int(fps)}',(40,50), cv2.FONT_HERSHEY_COMPLEX, 1,(0,0,255) , 2)

    cv2.imshow("img",img)
    cv2.waitKey(1)
