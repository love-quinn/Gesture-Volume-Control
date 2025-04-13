import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, MaxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.MaxHands = MaxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.MaxHands,
            min_detection_confidence=float(self.detectionCon),  # Certifique-se de usar float
            min_tracking_confidence=float(self.trackCon)        # Certifique-se de usar float
        )
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(RGBimg)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img
    def findPosition(self, img, handNo=0, draw=True):
        lmsList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                lmsList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (240, 1, 0), cv2.FILLED)
        return lmsList







def main():
    cTime = 0
    pTime = 0
    cap = cv2.VideoCapture(1)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)

        lmsList = detector.findPosition(img)
        if len(lmsList)!=0:
            print(lmsList[4])

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 3, (255, 0, 249), 3)

        cv2.imshow('image', img)
        cv2.waitKey(1)



if __name__ == '__main__':
    main()