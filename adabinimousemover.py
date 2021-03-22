import pyautogui
import keyboard
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)

while cap.isOpened():
  success, image = cap.read()
  if not success:
    continue

  image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

  image.flags.writeable = False
  results = hands.process(image)

  image.flags.writeable = True
  image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
  

  width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
  height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

  if results.multi_hand_landmarks:
    hand_landmarks = results.multi_hand_landmarks[0]
    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    screen_width, screen_height = pyautogui.size()
    x = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x * screen_width
    y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * screen_height

    x_cord = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x * width
    y_cord = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * height

    image = cv2.circle(image, (int(x_cord), int(y_cord)), 10, (255, 255, 0), -1)
    
    pyautogui.moveTo(x, y)
  
  cv2.imshow('AdabiniMouseMover', image)
  
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

hands.close()
cap.release()
