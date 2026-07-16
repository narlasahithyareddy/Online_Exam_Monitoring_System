status = "Not Started"

while True:

    print("\n1.Start")
    print("2.Pause")
    print("3.Resume")
    print("4.End")
    print("5.Exit")

    choice = int(input("Enter Choice: "))

    if choice == 1:
        if status == "Not Started":
            status = "Started"
            print("Exam Started")
        else:
            print("Already Started")

    elif choice == 2:
        if status == "Started":
            status = "Paused"
            print("Exam Paused")
        else:
            print("Cannot Pause")

    elif choice == 3:
        if status == "Paused":
            status = "Started"
            print("Exam Resumed")
        else:
            print("Cannot Resume")

    elif choice == 4:
        if status == "Started" or status == "Paused":
            status = "Ended"
            print("Exam Ended")
        else:
            print("Exam Not Started")

    elif choice == 5:
        break