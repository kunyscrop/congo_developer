import cv2
import mediapipe as mp
import subprocess
import math
from collections import deque

# Setup
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Track fingertip positions
trail = deque(maxlen=30)  # Store last 30 positions

def is_circle(trail):
    if len(trail) < 30:
        return False
    # Calculate center
    x_vals = [p[0] for p in trail]
    y_vals = [p[1] for p in trail]
    center_x = sum(x_vals) / len(x_vals)
    center_y = sum(y_vals) / len(y_vals)

    # Calculate average radius
    radii = [math.hypot(p[0] - center_x, p[1] - center_y) for p in trail]
    avg_radius = sum(radii) / len(radii)

    # Check if all points are close to the average radius
    return all(abs(r - avg_radius) < 20 for r in radii)

vs_code_opened = False

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm = hand_landmarks.landmark
            x = int(lm[8].x * w)
            y = int(lm[8].y * h)
            trail.append((x, y))

            cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
            for i in range(1, len(trail)):
                cv2.line(img, trail[i - 1], trail[i], (255, 0, 0), 2)

            if is_circle(trail) and not vs_code_opened:
                subprocess.Popen("code")  # Launch VS Code
                vs_code_opened = True
                cv2.putText(img, "VS Code Launched!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Circle Gesture Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()