import cv2
import mediapipe as mp
import pyautogui

# Setup
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Define keys
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
        ["Z", "X", "C", "V", "B", "N", "M"]]

def draw_keyboard(img):
    key_positions = []
    for i, row in enumerate(keys):
        for j, key in enumerate(row):
            x = 60 + j * 60
            y = 100 + i * 60
            cv2.rectangle(img, (x, y), (x + 50, y + 50), (200, 200, 200), -1)
            cv2.putText(img, key, (x + 15, y + 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            key_positions.append((key, x, y, x + 50, y + 50))
    return key_positions

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    key_boxes = draw_keyboard(img)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm = hand_landmarks.landmark
            h, w, _ = img.shape
            x = int(lm[8].x * w)
            y = int(lm[8].y * h)

            cv2.circle(img, (x, y), 10, (0, 255, 0), -1)

            for key, x1, y1, x2, y2 in key_boxes:
                if x1 < x < x2 and y1 < y < y2:
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), -1)
                    cv2.putText(img, key, (x1 + 15, y1 + 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    pyautogui.press(key.lower())

            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()