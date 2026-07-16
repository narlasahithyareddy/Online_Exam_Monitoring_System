id = input("Candidate ID: ")
name = input("Name: ")
email = input("Email: ")

file = open("candidate.txt", "a")

file.write(id + "," + name + "," + email + "\n")

file.close()

print("Candidate Saved")

print("\nAll Candidates")

file = open("candidate.txt", "r")

for line in file:
    print(line.strip())

file.close()

search = input("\nEnter Candidate ID to Search: ")

file = open("candidate.txt", "r")

found = False

for line in file:

    data = line.strip().split(",")

    if data[0] == search:

        print("Candidate Found")

        print("ID:", data[0])
        print("Name:", data[1])
        print("Email:", data[2])

        found = True

if not found:
    print("Candidate Not Found")

file.close()