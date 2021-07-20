import cv2
import mediapipe as mp

"""
    This is a module to use in hand tracking projects, call it by:
        import cv2
        import mediapipe as mp
        import handTrackingModule as htm
        
        cap = cv2.VideoCapture(0)
        detector = htm.handDetector()
        while True:
            success, img = cap.read()
            img = detector.findHands(img)
            lmList = detector.getPosition(img)
            if len(lmList) != 0:
                print(lmList[4])
            cv2.imshow("Image", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
"""

class handDetector():
    def __init__(self, mode = False, maxNum = 2, detecConf = 0.8, trackConf = 0.5):
        self.mode = mode
        self.maxNum = maxNum
        self.detecConf = detecConf
        self.trackConf = trackConf
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxNum, self.detecConf, self.trackConf)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def getPosition(self, img, handNum = 0):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNum]
            for id, lm, in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                # if draw:
                #     cv2.circle(img, (cx,cy), 15, (255, 0, 0), cv2.FILLED)
        return lmList
def main():

    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.getPosition(img)
        if len(lmList) != 0:
            print(lmList[4])
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()