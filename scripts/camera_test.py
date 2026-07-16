import cv2
from pathlib import Path

photos_dir = Path(__file__).resolve().parent.parent / "photos"
photos_dir.mkdir(parents=True, exist_ok=True)

camera = cv2.VideoCapture(0)

while True:

    ret, frame = camera.read()

    if not ret:
        print("Failed to access camera")
        break

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1)

    # Press 'c' to capture photo
    if key == ord('c'):
        photo_path = photos_dir / "candidate.jpg"
        cv2.imwrite(str(photo_path), frame)
        print("Photo Saved Successfully!")
        print("Photo Path:", photo_path)
        break

    # Press 'q' to quit
    if key == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()