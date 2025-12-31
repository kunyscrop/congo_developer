import cv2
import mediapipe as mp
import pyautogui
import math

# Setup
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_draw = mp.solutions.drawing_utils

def get_landmark_coords(landmarks, index, w, h):
    return int(landmarks[index].x * w), int(landmarks[index].y * h)

def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks and results.multi_handedness:
        hands_data = list(zip(results.multi_hand_landmarks, results.multi_handedness))

        for hand_landmarks, handedness in hands_data:
            label = handedness.classification[0].label  # 'Left' or 'Right'
            lm = hand_landmarks.landmark

            index_tip = get_landmark_coords(lm, 8, w, h)
            thumb_tip = get_landmark_coords(lm, 4, w, h)

            cv2.circle(img, index_tip, 10, (255, 0, 0), -1)
            cv2.circle(img, thumb_tip, 10, (0, 255, 0), -1)

            # Gesture: pinch = action
            if distance(index_tip, thumb_tip) < 40:
                if label == 'Right':
                    pyautogui.click()
                    cv2.putText(img, 'Right Hand Click', (index_tip[0], index_tip[1] - 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                elif label == 'Left':
                    pyautogui.press('ctrl')
                    cv2.putText(img, 'Left Hand CTRL', (index_tip[0], index_tip[1] - 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Two-Hand Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()