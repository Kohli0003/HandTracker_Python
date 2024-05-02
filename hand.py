import cv2
import mediapipe as mp
import pyautogui
import math
import time

smoothening = 8

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
cam = cv2.VideoCapture(1)
screen_w, screen_h = pyautogui.size()

last_click_time = time.time()
click_interval = 2  # Set the minimum time interval between clicks (in seconds)

# Initialize variables for smoothing
smoothed_cursor_x, smoothed_cursor_y = 0, 0

while True:
    _, image = cam.read()
    image = cv2.flip(image, 1)
    image_h, image_w, _ = image.shape
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            index_4 = hand_landmark.landmark[4]
            index_8 = hand_landmark.landmark[8]
            index_12 = hand_landmark.landmark[12]
            index_16 = hand_landmark.landmark[16]

            x4, y4 = int(index_4.x * image_w), int(index_4.y * image_h)
            x8, y8 = int(index_8.x * image_w), int(index_8.y * image_h)
            x12, y12 = int(index_12.x * image_w), int(index_12.y * image_h)
            x16, y16 = int(index_16.x * image_w), int(index_16.y * image_h)

            cursor_x = int(x8 * screen_w / image_w)
            cursor_y = int(y8 * screen_h / image_h)

            # Apply smoothing to cursor movement
            smoothed_cursor_x = (smoothed_cursor_x + cursor_x) / 2
            smoothed_cursor_y = (smoothed_cursor_y + cursor_y) / 2

            pyautogui.moveTo(int(smoothed_cursor_x), int(smoothed_cursor_y))

            cv2.circle(image, (x4, y4), 5, (255, 0, 0), -1)  # Draw circle for index 4
            cv2.circle(image, (x8, y8), 5, (0, 0, 255), -1)  # Draw circle for index 8
            cv2.circle(image, (x12, y12), 5, (0, 255, 255), -1)
            cv2.circle(image, (x16, y16), 5, (255, 255, 255), -1)

            distance = math.sqrt((x8 - x4) ** 2 + (y8 - y4) ** 2)
            distance2 = math.sqrt((x12 - x4) ** 2 + (y12 - y4) ** 2)
            distance3 = math.sqrt((x16 - x4) ** 2 + (y16 - y4) ** 2)

            if distance < 22 and (time.time() - last_click_time) > click_interval:
                print("click")
                pyautogui.click()
                last_click_time = time.time()
            elif distance2 < 22:
                print("double click")
                pyautogui.doubleClick()
            elif distance3 < 30:
                print("tab switch")
                pyautogui.hotkey('command', 'tab')

    cv2.imshow("Hand Gesture Control", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
