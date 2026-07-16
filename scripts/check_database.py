from pathlib import Path
import sqlite3

base_dir = Path(__file__).resolve().parent.parent
connection = sqlite3.connect(str(base_dir / "database" / "exam.db"))

cursor = connection.cursor()

cursor.execute("SELECT * FROM Candidate")

rows = cursor.fetchall()

for row in rows:
    print(row)

connection.close()
