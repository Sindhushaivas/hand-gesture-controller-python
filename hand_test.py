import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    if results.multi_hand_landmarks:
         for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            if results.multi_hand_landmarks:
             for hand_landmarks in results.multi_hand_landmarks:
              mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            print(hand_landmarks.landmark[8])  
            x = hand_landmarks.landmark[8].x
            y = hand_landmarks.landmark[8].y

            print("Index Finger Tip:", x, y)
            import pyautogui

            x = hand_landmarks.landmark[8].x
            y = hand_landmarks.landmark[8].y

            screen_width, screen_height = pyautogui.size()
            screen_x = int(x * screen_width)
            screen_y = int(y * screen_height)

            current_x, current_y = pyautogui.position()
            smooth_x = current_x + (screen_x - current_x) // 3
            smooth_y = current_y + (screen_y - current_y) // 3

            pyautogui.moveTo(smooth_x, smooth_y)
            cv2.imshow("Camera Test", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
             break

cap.release()
cv2.destroyAllWindows()
