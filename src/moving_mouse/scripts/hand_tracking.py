import cv2
import mediapipe as mp
import handTrackingModule as htm
import math
import mouse

def calculateDistance(x1, y1, x2, y2):
    dist = math.sqrt((x2-x1)**2+(y2-y1)**2)
    return dist

def getMousePosition(xTip, yTip, delta = 50):
    # 1365, 767
    # 640, 480
    xMouse = ((640-xTip-delta) * 1365)/(640-2*delta)
    yMouse = (yTip * 767-delta)/(480-2*delta)
    return xMouse, yMouse

cap = cv2.VideoCapture(0)
detector = htm.handDetector()

Tip = 8
Phal = 7

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=False)
    lmList = detector.getPosition(img)

    if len(lmList) != 0:
        #print(lmList[4][1])
        xTip, yTip = lmList[Tip][1], lmList[Tip][2]
        xPhal, yPhal = lmList[Phal][1], lmList[Phal][2]
        cv2.circle(img, (xTip, yTip), 5, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (xPhal, yPhal), 5, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (xTip, yTip), (xPhal, yPhal), (0, 0, 255), 1)
        # print(lmList[Tip])
        if lmList[Tip] and lmList[Phal]:
            xMouse, yMouse = getMousePosition(xTip, yTip)
            mouse.move(xMouse, yMouse, absolute=True, duration=0.2)
            dist = calculateDistance(xTip, yTip, xPhal, yPhal)
            # print(mouse.get_position())
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
