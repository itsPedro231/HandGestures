import mediapipe as mp
import cv2
import math
import pyautogui as pag

def handTracking():
    video = cv2.VideoCapture(0) 
    global x1, y1, x2, y2   
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    draw = mp.solutions.drawing_utils

    while True:
        _, img = video.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(imgRGB)

        if result.multi_hand_landmarks:
            for lmks in result.multi_hand_landmarks:
                for id, lm in enumerate(lmks.landmark):
                    (h, w, _) = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    draw.draw_landmarks(img, lmks, mpHands.HAND_CONNECTIONS)

                    if id == 4:
                        polx, poly = cx, cy 
                    if id == 8:
                        indx, indy = cx, cy   
                    if id == 20:
                        pinx, piny = cx, cy           
                    #print("id:", id, " x:", cx, " y:", cy)
                midx1, midy1 = (polx + indx)//2, (poly + indy)//2
                midx2, midy2 = (polx + pinx)//2, (poly + piny)//2 
                
                # drawing
                cv2.circle(img, (polx, poly), 10, (255, 100, 0), cv2.FILLED)  
                cv2.circle(img, (indx, indy), 10, (255, 100, 0), cv2.FILLED)
                cv2.circle(img, (pinx, piny), 10, (255, 100, 0), cv2.FILLED)
                cv2.line(img, (polx, poly), (indx, indy), (255, 100, 0), 2)
                cv2.line(img, (polx, poly), (pinx, piny), (255, 100, 0), 2)
                cv2.circle(img, (midx1, midy1), 8, (255, 100, 0), cv2.FILLED)
                cv2.circle(img, (midx2, midy2), 8, (255, 100, 0), cv2.FILLED)

                length1 = math.hypot(indx - polx, indy - poly)
                length2 = math.hypot(pinx - polx, piny - poly)
                
                # disabled functions -----------
                # length3 = math.hypot(meiox - polx, meioy - poly)
                # length4 = math.hypot(anelx - polx, anely - poly)
                # -------------   
                
                if length1 < 40 and length2 > 70:
                    cv2.circle(img, (midx1, midy1), 8, (0, 255, 0), cv2.FILLED)
#                     pag.keyDown("space") # press space when thumb and index fingers are together  
                
                if length2 > 300:
                    cv2.circle(img, (polx, poly), 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(img, (pinx, piny), 10, (0, 0, 255), cv2.FILLED)
#                     pag.keyDown("right") # press right arrow when thumb and little fingers are streched

                if length2 < 40:
                    cv2.circle(img, (midx2, midy2), 8, (0, 255, 255), cv2.FILLED)
#                     pag.keyDown("left") # press left arrow when thumb and little fingers are together
                    
        cv2.imshow("Image", img)
        cv2.waitKey(1)

handTracking()

