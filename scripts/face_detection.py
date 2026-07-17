import cv2
import sqlite3
from datetime import datetime
from pathlib import Path

script_dir = Path(__file__).resolve().parent
base_dir = script_dir.parent

cascade_path = base_dir / "haarcascade" / "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(str(cascade_path))

if face_cascade.empty():
    print("Error: Haar Cascade XML file not loaded!")
    exit()

photos_dir = base_dir / "photos"
photos_dir.mkdir(parents=True, exist_ok=True)

candidate_id = 101
face_missing = False
absence_start = None
absence_duration = 0
face_detected_count = 0
face_not_detected_count = 0

camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100,100))

    current_date = datetime.now().strftime("%d-%m-%Y")
    current_time = datetime.now().strftime("%I:%M:%S %p")

    if len(faces) > 0:
        if face_missing:
            face_detected_count += 1
        if face_detected_count == 0 and face_not_detected_count == 0:
            face_detected_count = 1

        face_missing = False
        absence_start = None
        absence_duration = 0

        cv2.putText(frame,"Face Detected",(20,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    else:
        if absence_start is None:
            absence_start = datetime.now()

        absence_duration = (datetime.now()-absence_start).seconds

        cv2.putText(frame,"Face Not Detected",(20,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

        if not face_missing:
            face_not_detected_count += 1

            db_path = base_dir / "database" / "exam.db"
            conn = sqlite3.connect(str(db_path))
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO EventLog(candidate_id,event_type,timestamp,remarks) VALUES (?,?,?,?)",
                (candidate_id,"Face Not Detected",datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"Candidate face is absent")
            )

            conn.commit()
            conn.close()

            face_missing = True

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

    cv2.putText(frame,f"Date: {current_date}",(20,80),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
    cv2.putText(frame,f"Time: {current_time}",(20,120),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
    cv2.putText(frame,f"Absence Duration: {absence_duration} sec",(20,160),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,0),2)
    cv2.putText(frame,f"Face Not Detected Count: {face_not_detected_count}",(20,200),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,255),2)
    cv2.putText(frame,f"Face Detected Count: {face_detected_count}",(20,240),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)

    cv2.imshow("Face Detection", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("c"):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        cv2.imwrite(str(photos_dir / f"capture_{ts}.png"), frame)

camera.release()
cv2.destroyAllWindows()
