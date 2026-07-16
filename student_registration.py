students = []

while True:
    print("\n===== Student Registration System =====")
    print("1. Register Student")
    print("2. Display Students")
    print("3. Search Student")
    print("4. Delete Student")
    print("5. Exit")

    choice = int(input("Enter Choice: "))

    if choice == 1:
        sid = input("Enter Student ID: ")
        name = input("Enter Name: ")
        age = input("Enter Age: ")

        student = {
            "ID": sid,
            "Name": name,
            "Age": age
        }

        students.append(student)
        print("Student Registered Successfully!")

    elif choice == 2:
        if len(students) == 0:
            print("No Students Found")
        else:
            for student in students:
                print(student)

    elif choice == 3:
        sid = input("Enter Student ID: ")

        found = False

        for student in students:
            if student["ID"] == sid:
                print(student)
                found = True
                break

        if not found:
            print("Student Not Found")

    elif choice == 4:
        sid = input("Enter Student ID: ")

        found = False

        for student in students:
            if student["ID"] == sid:
                students.remove(student)
                print("Deleted Successfully")
                found = True
                break

        if not found:
            print("Student Not Found")

    elif choice == 5:
        print("Thank You")
        break

    else:
        print("Invalid Choice")