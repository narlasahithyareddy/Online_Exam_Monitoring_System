import sqlite3

connection = sqlite3.connect("database/exam.db")

cursor = connection.cursor()

cursor.execute("SELECT * FROM Candidate")

rows = cursor.fetchall()

for row in rows:
    print(row)

connection.close()
