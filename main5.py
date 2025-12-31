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
show_guides = True  # Touche 'g' pour basculer

# Noms et actions des doigts
finger_info = {
    4: ("Pouce", "Ctrl / Clic"),
    8: ("Index", "Souris / Win"),
    12: ("Majeur", "Shift / Double clic"),
    16: ("Annulaire", "Tab / Clic droit"),
    20: ("Auriculaire", "Win / Scroll")
}

finger_colors = {
    4: (0, 255, 255),
    8: (255, 0, 0),
    12: (0, 255, 0),
    16: (255, 0, 255),
    20: (0, 165, 255)
}

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

            # Affichage des guides visuels
            if show_guides:
                for id in finger_info:
                    cx, cy = lmList[id]
                    name, action = finger_info[id]
                    color = finger_colors[id]
                    cv2.circle(img, (cx, cy), 10, color, cv2.FILLED)
                    cv2.putText(img, f"{name}: {action}", (cx + 10, cy - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            if handType == 'Right':
                index_finger = lmList[8]
                x = int(index_finger[0] * screen_w / wCam)
                y = int(index_finger[1] * screen_h / hCam)
                pyautogui.moveTo(x, y)

                thumb_tip = lmList[4]
                if distance(thumb_tip, index_finger) < 40:
                    pyautogui.click()

                if distance(lmList[12], thumb_tip) < 40:
                    pyautogui.doubleClick()
                if distance(lmList[16], thumb_tip) < 40:
                    pyautogui.rightClick()
                if distance(lmList[20], thumb_tip) < 40:
                    pyautogui.scroll(-10)

            elif handType == 'Left':
                thumb_tip = lmList[4]

                if distance(thumb_tip, lmList[8]) < 40:
                    pyautogui.keyDown('ctrl')
                else:
                    pyautogui.keyUp('ctrl')

                if distance(thumb_tip, lmList[12]) < 40:
                    pyautogui.keyDown('shift')
                else:
                    pyautogui.keyUp('shift')

                if distance(thumb_tip, lmList[16]) < 40:
                    pyautogui.press('tab')

                if distance(thumb_tip, lmList[20]) < 40:
                    pyautogui.press('win')

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow("Control PC with Hands", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('g'):
        show_guides = not show_guides
    if key == ord('q'):
        break   