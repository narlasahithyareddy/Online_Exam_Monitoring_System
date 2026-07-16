from flask import Flask, render_template, request, redirect
import sqlite3
import re
import cv2
import os
from datetime import datetime

app = Flask(__name__)


def capture_photo(candidate_id):

    if not os.path.exists("photos"):
        os.makedirs("photos")

    camera = cv2.VideoCapture(0)

    while True:

        ret, frame = camera.read()

        cv2.imshow("Capture Photo", frame)

        key = cv2.waitKey(1)

        if key == ord('c'):

            photo_path = f"photos/{candidate_id}.jpg"

            cv2.imwrite(photo_path, frame)

            break

    camera.release()
    cv2.destroyAllWindows()

    return photo_path


# ---------------- Home ----------------
@app.route("/")
def home():
    return render_template("register.html")


# ---------------- Register ----------------
@app.route("/register", methods=["POST"])
def register():

    candidate_id = request.form["candidate_id"]
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    photo_path = capture_photo(candidate_id)

    # ---------- Validation ----------

    # Empty Fields
    if candidate_id == "" or name == "" or email == "" or password == "":
        return "All fields are required!"

    # Email Validation
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not re.match(email_pattern, email):
        return "Invalid Email Format!"

    # Password Validation
    if password == "":
        return "Password cannot be empty!"

    # ---------- Database ----------

    connection = sqlite3.connect("database/exam.db")
    cursor = connection.cursor()

    # Check Duplicate Email
    cursor.execute(
        "SELECT * FROM Candidate WHERE email=?",
        (email,)
    )

    user = cursor.fetchone()

    if user:
        connection.close()
        return "Email already registered! Please use another email."

    # Insert Candidate
    cursor.execute("""
        INSERT INTO Candidate(candidate_id, name, email, password, photo_path)
        VALUES (?, ?, ?, ?, ?)
    """, (candidate_id, name, email, password, photo_path))

    connection.commit()
    connection.close()

    # Redirect to Login Page
    return redirect("/login")


# ---------------- Login Page ----------------
@app.route("/login")
def login_page():
    return render_template("login.html")


# ---------------- Login ----------------
@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]
    password = request.form["password"]

    connection = sqlite3.connect("database/exam.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT name FROM Candidate WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()

    connection.close()

    if user:
        return redirect("/dashboard")
    else:
        return "Invalid Email or Password"


# ---------------- Dashboard ----------------
@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        candidate="Raghu"
    )


# Open Session Page
@app.route("/session")
def session():
    return render_template("session.html")

# Start Exam
@app.route("/start_exam", methods=["POST"])
def start_exam():

    connection = sqlite3.connect("database/exam.db")
    cursor = connection.cursor()

    candidate_id = 101

    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO Session(candidate_id, start_time, status)
        VALUES (?, ?, ?)
    """, (candidate_id, start_time, "Started"))

    connection.commit()
    connection.close()

    return "Exam Started Successfully!"

# Pause Exam
@app.route("/pause_exam", methods=["POST"])
def pause_exam():

    connection = sqlite3.connect("database/exam.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE Session
        SET status=?
        WHERE session_id=(SELECT MAX(session_id) FROM Session)
    """, ("Paused",))

    connection.commit()
    connection.close()

    return "Exam Paused Successfully!"

# Resume Exam
@app.route("/resume_exam", methods=["POST"])
def resume_exam():

    connection = sqlite3.connect("database/exam.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE Session
        SET status=?
        WHERE session_id=(SELECT MAX(session_id) FROM Session)
    """, ("Resumed",))

    connection.commit()
    connection.close()

    return "Exam Resumed Successfully!"

# End Exam
@app.route("/end_exam", methods=["POST"])
def end_exam():

    connection = sqlite3.connect("database/exam.db")
    cursor = connection.cursor()

    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        UPDATE Session
        SET end_time=?, status=?
        WHERE session_id=(SELECT MAX(session_id) FROM Session)
    """, (end_time, "Ended"))

    connection.commit()
    connection.close()

    return "Exam Ended Successfully!"


# ---------------- Run Flask ----------------
if __name__ == "__main__":
    app.run(debug=True)