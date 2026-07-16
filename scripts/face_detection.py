# face_detection.py
import cv2
import sqlite3
from datetime import datetime
from pathlib import Path

script_dir = Path(__file__).resolve().parent
base_dir = script_dir.parent

# Load Haar Cascade
cascade_path = base_dir / "haarcascade" / "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(str(cascade_path))

if face_cascade.empty():
    print("Error: Haar Cascade XML file not loaded!")
    exit()

# Create photos folder if needed
photos_dir = base_dir / "photos"
photos_dir.mkdir(parents=True, exist_ok=True)

candidate_id = 101
face_missing = False
absence_start = None
absence_duration = 0

# Open Webcam
camera = cv2.VideoCapture(0)

while True:

    ret, frame = camera.read()

    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))

    # Convert image to Grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # Detect Faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100)
    )

    current_time = datetime.now().strftime("%H:%M:%S")
    absence_duration = 0

    if len(faces) > 0:

        face_missing = False
        absence_start = None
        absence_duration = 0

        cv2.putText(
            frame,
            "Face Detected",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    else:

        if absence_start is None:
            absence_start = datetime.now()

        absence_duration = (
            datetime.now() - absence_start
        ).seconds

        current_time = datetime.now().strftime("%H:%M:%S")

        cv2.putText(
            frame,
            "Face Not Detected",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        if not face_missing:

            db_path = base_dir / "database" / "exam.db"
            connection = sqlite3.connect(str(db_path))
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO EventLog(candidate_id, event_type, timestamp, remarks)
                VALUES (?, ?, ?, ?)
            """, (
                candidate_id,
                "Face Not Detected",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Candidate face is absent"
            ))

            connection.commit()
            connection.close()

            print("Face Not Detected Event Logged!")

            face_missing = True

    # Draw Bounding Box
    for (x, y, w, h) in faces:
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

    cv2.putText(
        frame,
        f"Time: {current_time}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Absence Duration: {absence_duration} sec",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2
    )

    # Show Video
    cv2.imshow("Face Detection", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{timestamp}.png"
        filepath = photos_dir / filename
        cv2.imwrite(str(filepath), frame)
        print(f"Saved capture: {filepath}")

camera.release()
cv2.destroyAllWindows()
