import random
import maskpass
import os
import hashlib
import time
import re

COOLDOWN_TIME_LOGIN = 60
COOLDOWN_TIME_CODE = 30
MAX_ATTEMPTS = 3
USER_DATA_FILE = "register_user.txt"

# ----------------- Login Class -----------------
class Login:
    def __init__(self, database=USER_DATA_FILE):
        self.database = database

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify(self, username, password):
        if not os.path.exists(self.database):
            print("Error: User data file not found.")
            return False

        try:
            with open(self.database, "r") as file:
                users = {}
                for line in file:
                    user_data = eval(line.strip())
                    users[user_data['username']] = user_data['password']
        except Exception as e:
            print(f"Error reading user data: {e}")
            return False

        if username not in users:
            print("!!! Invalid username !!!")
            return "username_invalid"

        entered_hashed_password = self.hash_password(password)
        if entered_hashed_password != users[username]:
            return "password_invalid"

        return True

    @staticmethod
    def generate_random_code(length=6):
        characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        return ''.join(random.choice(characters) for _ in range(length))


# ----------------- UserManager Class -----------------
class UserManager:
    def __init__(self, file_name=USER_DATA_FILE):
        self.file_name = file_name

    def is_user_exist(self, identifier):
        try:
            with open(self.file_name, 'r') as file:
                for line in file:
                    user_data = eval(line.strip())
                    if identifier in (user_data['username'], user_data['phone']):
                        return True
        except FileNotFoundError:
            pass
        return False

    def set_password(self, identifier):
        new_password = input("Enter a new password: ")
        if self.is_strong_password(new_password):
            updated_users = []
            with open(self.file_name, 'r') as file:
                for line in file:
                    user_data = eval(line.strip())
                    if identifier in (user_data['username'], user_data['phone']):
                        user_data['password'] = Login.hash_password(new_password)
                    updated_users.append(user_data)

            with open(self.file_name, 'w') as file:
                for user in updated_users:
                    file.write(str(user) + "\n")

            print("Password updated successfully!")
        else:
            print("Password is not strong enough. Please try again.")

    @staticmethod
    def is_strong_password(password):
        if len(password) < 8 or not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password) or not re.search(r'\d', password):
            return False
        if not re.search(r'[@$!%*?&#]', password):
            return False
        return True


# ----------------- UserRegisteration Class -----------------
class UserRegisteration:
    def __init__(self, file_name=USER_DATA_FILE):
        self.file_name = file_name

    def user_register(self):
        firstname = input("First name: ").strip()
        lastname = input("Last name: ").strip()

        while True:
            username = input("Username: ").strip()
            if self.check_duplicate_username(username):
                print("Username already taken, please choose a different one.")
            else:
                break

        while True:
            password = input("Enter your password: ").strip()
            confirm_password = input("Confirm your password: ").strip()

            if password != confirm_password:
                print("Error: Passwords do not match. Please try again.")
                continue

            if UserManager.is_strong_password(password):
                hashed_password = Login.hash_password(password)
                break
            else:
                print("Password is not strong enough. Please try again.")

        while True:
            phone = input("Phone number: +855 ").strip()
            if self.check_phone_number(phone):
                phone = "+855 " + phone
                break
            print("Error: Invalid phone number. Please enter 8–9 digits after +855.")

        user_data = {
            'firstname': firstname,
            'lastname': lastname,
            'username': username,
            'phone': phone,
            'password': hashed_password,
        }

        self.save_user_data(user_data)
        print("Registered Successfully!")

    def check_duplicate_username(self, username):
        try:
            with open(self.file_name, 'r') as file:
                for line in file:
                    user_data = eval(line.strip())
                    if user_data['username'] == username:
                        return True
        except FileNotFoundError:
            pass
        return False

    @staticmethod
    def check_phone_number(phone_number):
        return phone_number.isdigit() and 8 <= len(phone_number) <= 9

    def save_user_data(self, user_data):
        try:
            with open(self.file_name, "a") as file:
                file.write(str(user_data) + "\n")
        except OSError as e:
            print(f"Error saving user data: {e}")


# ----------------- Main Workflow -----------------
def main():
    print("Welcome to the System!")
    print("[1] Register")
    print("[2] Login")
    print("[3] Reset Password")

    choice = input("Choose an option: ").strip()
    if choice == '1':
        reg = UserRegisteration()
        reg.user_register()
    elif choice == '2':
        login = Login()
        username = input("Enter username: ").strip()
        password = maskpass.askpass(mask="*").strip()
        if login.verify(username, password) == True:
            code = login.generate_random_code()
            print(f"Your verification code is: {code}")
            entered_code = input("Enter the verification code: ").strip()
            if entered_code == code:
                print("Login successful!")
            else:
                print("Invalid verification code.")
    elif choice == '3':
        manager = UserManager()
        identifier = input("Enter your username or phone number: ").strip()
        if manager.is_user_exist(identifier):
            manager.set_password(identifier)
        else:
            print("User not found.")
    else:
        print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
