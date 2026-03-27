# Motion-Detection-Projects
A collection of real-time motion and gesture detection projects using Python, OpenCV, and MediaPipe.
# 🖐️ Motion Detection Projects

A collection of real-time motion and gesture detection projects using Python, OpenCV, and MediaPipe.

---

## 📁 Projects

### 1. Index Finger Tracker
> Track the tip of your index finger in real time using your webcam.

| Detail | Info |
|---|---|
| File | `index_finger_tracker.py` |
| Input | Webcam |
| Output | Live video with a dot on your index fingertip |
| Model | MediaPipe Hand Landmarker |

---

## 🛠️ Tech Stack

- **Python** — Core language
- **OpenCV** — Webcam capture and drawing
- **MediaPipe** — AI-powered hand and gesture detection

---

## ⚙️ Setup & Installation

**1. Clone the repo**
```bash
git clone https://github.com/your-username/motion-detection-projects.git
cd motion-detection-projects
```

**2. Install dependencies**
```bash
pip install opencv-python mediapipe
```

**3. Download the MediaPipe hand model**

Download `hand_landmarker.task` from the [MediaPipe releases page](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker) and place it in the project root.

**4. Run a project**
```bash
python index_finger_tracker.py
```

> **Note:** Press `Q` to quit the webcam window.

---

## 🔧 Configuration

In `index_finger_tracker.py` you can tweak these settings:

```python
cv2.VideoCapture(1)          # Change to 0 for built-in webcam, 1 for external
num_hands=1                  # Increase to track more hands
min_hand_detection_confidence=0.8   # Lower = detects more but less accurate
```

---

## 📌 How It Works

1. Webcam frame is captured and flipped (mirror effect)
2. MediaPipe AI model scans the frame and finds 21 hand landmarks
3. Landmark `8` (index fingertip) position is extracted
4. A dot is drawn on screen at that position in real time

---

## 🗺️ Roadmap

- [x] Index finger tracker
- [ ] All finger tracker
- [ ] Gesture recognition (thumbs up, peace sign, etc.)
- [ ] Mouse control using finger
- [ ] Two-hand gesture detection

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
