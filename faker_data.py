from faker import Faker
import csv
import random

fake = Faker()

subjects = [
    "Python",
    "Java",
    "Artificial Intelligence",
    "Machine Learning",
    "Data Science",
    "Cloud Computing"
]

with open("candidates.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Candidate ID",
        "Name",
        "Email",
        "Age",
        "Exam Subject"
    ])

    for i in range(1, 21):

        writer.writerow([
            i,
            fake.name(),
            fake.email(),
            random.randint(18, 30),
            random.choice(subjects)
        ])

print("20 Candidate Records Generated Successfully!")