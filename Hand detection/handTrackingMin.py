import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

# making hands object
mpHands = mp.solutions.hands
hands = mpHands.Hands()

# drawing dot and line 
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

# eternal loop
while True:
    # reading the frame from camera
    success ,img = cap.read()
    # converting color image to grayscale image
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    # getting hand detection results
    results = hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w),int(lm.y * h)
                # print(id, cx,cy)


            # circle on landmak with id no
                if id== 4:
                    cv2.circle(img , (cx,cy), 15 ,(255,0,255), cv2.FILLED)

            # drawing line in img
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)


    # fps calculation
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    #adding fps in video or in img
    cv2.putText(img, str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)


    # showimg video as a part of img but with higher fps seems like video 
    cv2.imshow("Image",img)
    cv2.waitKey(1)