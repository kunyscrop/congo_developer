import cv2
import mediapipe as mp
import pyautogui
import math

# Initialisation
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm = hand_landmarks.landmark
            h, w, _ = img.shape

            # Index fingertip (id 8) and thumb tip (id 4)
            x1, y1 = int(lm[8].x * w), int(lm[8].y * h)
            x2, y2 = int(lm[4].x * w), int(lm[4].y * h)

            # Dessin
            cv2.circle(img, (x1, y1), 10, (255, 0, 0), -1)
            cv2.circle(img, (x2, y2), 10, (0, 255, 0), -1)
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 2)

            # Si les doigts sont proches → appuie sur une touche
            if distance((x1, y1), (x2, y2)) < 40:
                pyautogui.press('space')  # Simule la touche espace
                cv2.putText(img, 'SPACE', (x1, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Clavier Camera", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()