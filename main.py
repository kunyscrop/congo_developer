import cv2
import mediapipe as mp
import pyautogui

# Initialisation
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

screen_w, screen_h = pyautogui.size()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Miroir
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = []
            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * wCam), int(lm.y * hCam)
                lmList.append((cx, cy))

            # Déplacement souris avec l'index
            index_finger = lmList[8]  # Index tip
            x = int(index_finger[0] * screen_w / wCam)
            y = int(index_finger[1] * screen_h / hCam)
            pyautogui.moveTo(x, y)

            # Clic si pouce et index sont proches
            thumb_tip = lmList[4]
            distance = ((thumb_tip[0] - index_finger[0])**2 + (thumb_tip[1] - index_finger[1])**2)**0.5
            if distance < 40:
                pyautogui.click()

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow("Control PC with Hand", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break