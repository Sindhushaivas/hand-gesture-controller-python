import cv2
import mediapipe as mp
import pyautogui
import math

# Setup
pyautogui.FAILSAFE = False
cap = cv2.VideoCapture(0)
cap.set(3, 320)  # width
cap.set(4, 240)  # height

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()

import time

last_action_time = 0
cooldown = 0.5 # 1 second delay between actions

while True:
    success, frame = cap.read()
    current_time = time.time()
    if not success:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # -------------------- CURSOR CONTROL --------------------
            index_tip = hand_landmarks.landmark[8]
            x = int(index_tip.x * screen_width)
            y = int(index_tip.y * screen_height)

            current_x, current_y = pyautogui.position()
            smooth_x = current_x + (x - current_x) // 3
            smooth_y = current_y + (y - current_y) // 3
            pyautogui.moveTo(smooth_x, smooth_y)

            # -------------------- FINGER UP DETECTION --------------------
            finger_tips = [8, 12, 16, 20]  # index, middle, ring, pinky
            finger_pips = [6, 10, 14, 18]

            fingers_up = []
            for tip, pip in zip(finger_tips, finger_pips):
                if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
                    fingers_up.append(1)  # finger is up
                else:
                    fingers_up.append(0)  # finger is down

            # Thumb detection (y coordinate for up/down)
            thumb_tip = hand_landmarks.landmark[4]
            thumb_ip = hand_landmarks.landmark[3]

            # -------------------- VOLUME CONTROL --------------------
            if thumb_tip.y < thumb_ip.y and fingers_up == [0, 0, 0, 0]:  # Thumb up
                pyautogui.press("volumeup")
            elif thumb_tip.y > thumb_ip.y and fingers_up == [0, 0, 0, 0]:  # Thumb down
                pyautogui.press("volumedown")

            # -------------------- PLAY / PAUSE --------------------
            if fingers_up == [1, 1, 1, 1]:  # Open hand → play
                pyautogui.press("playpause")
            elif fingers_up == [0, 0, 0, 0]:  # Fist → pause
                pyautogui.press("playpause")

            # -------------------- EXIT --------------------
            if fingers_up[0] == 1 and fingers_up[1] == 1 and fingers_up[2] == 0 and fingers_up[3] == 0:
                print("Peace detected → Exiting")
                cap.release()
                cv2.destroyAllWindows()
                exit()

    cv2.imshow("Hand Gesture Controller", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()