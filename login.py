users = {
    "raghu": "1234",
    "admin": "admin123",
    "student": "pass123"
}

attempts = 0

while attempts < 3:

    username = input("Username: ")
    password = input("Password: ")

    if username in users and users[username] == password:
        print("Login Successful")
        break

    else:
        attempts += 1
        print("Invalid Credentials")
        print("Attempts Left:", 3 - attempts)

if attempts == 3:
    print("Account Locked")