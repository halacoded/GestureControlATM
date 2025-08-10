import cv2
import pyautogui
import mediapipe as mp

# Use DirectShow backend for USB webcam reliability
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

mp_drawing = mp.solutions.drawing_utils

print("🖐️ Starting hand gesture detection... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Failed to grab frame.")
        break

    # Flip frame for mirror effect
    frame = cv2.flip(frame, 1)

    # Convert to RGB for MediaPipe
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get Y positions of index finger tip and thumb tip
            index_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

            # Determine gesture
            if index_y < thumb_y - 0.05:
                gesture = 'pointing up'
                pyautogui.press('volumeup')
            elif index_y > thumb_y + 0.05:
                gesture = 'pointing down'
                pyautogui.press('volumedown')
            else:
                gesture = 'neutral'

            # Display gesture on frame
            cv2.putText(frame, f'Gesture: {gesture}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Hand Gesture Control', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("👋 Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
