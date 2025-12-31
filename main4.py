import cv2
import mediapipe as mp
import pyautogui

# Initialisation
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=2)
mpDraw = mp.solutions.drawing_utils

screen_w, screen_h = pyautogui.size()

def get_finger_positions(handLms):
    return [(int(lm.x * wCam), int(lm.y * hCam)) for lm in handLms.landmark]

def distance(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks and results.multi_handedness:
        for i, handLms in enumerate(results.multi_hand_landmarks):
            handType = results.multi_handedness[i].classification[0].label  # 'Left' or 'Right'
            lmList = get_finger_positions(handLms)

            if handType == 'Right':
                index_finger = lmList[8]
                x = int(index_finger[0] * screen_w / wCam)
                y = int(index_finger[1] * screen_h / hCam)
                pyautogui.moveTo(x, y)

                thumb_tip = lmList[4]
                if distance(thumb_tip, index_finger) < 40:
                    pyautogui.click()

                # Autres doigts pour actions personnalisées
                if distance(lmList[12], lmList[4]) < 40:  # Majeur
                    pyautogui.doubleClick()
                if distance(lmList[16], lmList[4]) < 40:  # Annulaire
                    pyautogui.rightClick()
                if distance(lmList[20], lmList[4]) < 40:  # Auriculaire
                    pyautogui.scroll(-10)

            elif handType == 'Left':
                # Simuler des touches clavier selon la position des doigts
                if distance(lmList[4], lmList[8]) < 40:
                    pyautogui.keyDown('ctrl')
                else:
                    pyautogui.keyUp('ctrl')
    
                if distance(lmList[12], lmList[4]) < 40:
                    pyautogui.keyDown('shift')
                else:
                    pyautogui.keyUp('shift')

                if distance(lmList[16], lmList[4]) < 40:
                    pyautogui.press('tab')

                if distance(lmList[20], lmList[4]) < 40:
                    pyautogui.press('win')

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow("Control PC with Hands", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break