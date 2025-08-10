import cv2
import pyautogui
import mediapipe as mp

# Start webcam capture
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera not detected.")
else:
    print("✅ Camera is working. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to grab frame.")
            break

        cv2.imshow("Camera Test", frame)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()