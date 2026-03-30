import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import urllib.request
import os

# --- Download the gesture model if not present ---
MODEL_PATH = "gesture_recognizer.task"
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task"

if not os.path.exists(MODEL_PATH):
    print("Downloading gesture model...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print("Done.")

# --- Finger-based gesture logic ---
FINGER_TIPS = [8, 12, 16, 20]
FINGER_PIPS = [6, 10, 14, 18]

def fingers_up(landmarks):
    f = []
    f.append(1 if landmarks[4].x < landmarks[3].x else 0)  # thumb
    for tip, pip in zip(FINGER_TIPS, FINGER_PIPS):
        f.append(1 if landmarks[tip].y < landmarks[pip].y else 0)
    return f

def classify_custom(landmarks):
    f = fingers_up(landmarks)
    gestures = {
        (0,0,0,0,0): "Fist",
        (1,1,1,1,1): "Open Hand",
        (1,0,0,0,0): "Thumbs Up",
        (0,1,1,0,0): "Peace Sign",
        (0,1,0,0,0): "Pointing",
        (0,1,0,0,1): "Rock On",
        (1,1,0,0,1): "Spider-Man",
        (0,0,0,0,1): "Pinky",
    }
    return gestures.get(tuple(f), "Unknown")

# --- Pure OpenCV landmark drawing (no mediapipe.framework needed) ---
def draw_landmarks_on_frame(frame, hand_landmarks_list):
    h, w, _ = frame.shape
    connections = [
        (0,1),(1,2),(2,3),(3,4),
        (0,5),(5,6),(6,7),(7,8),
        (0,9),(9,10),(10,11),(11,12),
        (0,13),(13,14),(14,15),(15,16),
        (0,17),(17,18),(18,19),(19,20),
        (5,9),(9,13),(13,17)
    ]
    for hand_landmarks in hand_landmarks_list:
        pts = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks]
        for a, b in connections:
            cv2.line(frame, pts[a], pts[b], (0, 200, 255), 2)
        for pt in pts:
            cv2.circle(frame, pt, 5, (255, 255, 255), -1)

# --- Main ---
def main():
    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.GestureRecognizerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.IMAGE,
        num_hands=2
    )

    cap = cv2.VideoCapture(0)
    print("Press 'q' to quit.")

    with vision.GestureRecognizer.create_from_options(options) as recognizer:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

            result = recognizer.recognize(mp_image)

            if result.hand_landmarks:
                draw_landmarks_on_frame(frame, result.hand_landmarks)

                for i, hand_landmarks in enumerate(result.hand_landmarks):
                    gesture = classify_custom(hand_landmarks)
                    h, w, _ = frame.shape
                    cx = int(hand_landmarks[0].x * w)
                    cy = int(hand_landmarks[0].y * h)
                    cv2.putText(frame, gesture, (cx - 50, cy - 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

            cv2.imshow("Gesture Recognition", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()