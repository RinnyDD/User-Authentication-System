import os
import sys
import json
import re
sys.path.append(os.path.abspath(r"User-Authentication-System/modules"))
from Register import UserRegisteration  # Importing the register function from Register.py
from base_register import User


class UserManager:
    def __init__(self, filename=r"User-Authentication-System/main/database.txt"):
       self.filename = filename
       self.users = self.load_users()
    def load_users(self):
        users = {}
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                for line in file:
                    user_data = json.loads(line.strip())
                    username = user_data["username"]
                    users[username] = user_data
        return users

    def is_user_exist(self, identifier):
        for username, data in self.users.items():
            if identifier in (username, data["phone"]):
                return True
        return False

    def set_password(self, identifier):
        attempts = 0
        while attempts < 3:
            new_password = input("Enter a new password: ").strip()
            if self.is_strong_password(new_password):
                confirm_password = input("Confirm your new password: ").strip()
                if new_password == confirm_password:
                    for username, data in self.users.items():
                        if identifier in (username, data["phone"]):
                            data["password"] = new_password
                            self.save_users()
                            print("Password updated successfully!")
                            return
                else:
                    print("Error: Passwords do not match. Please try again.")
            else:
                print("Password is not strong enough. Use a combination of uppercase, lowercase, numbers, and special characters.")
            attempts += 1
            print(f"Remaining attempts: {3 - attempts}")
            print("Too many failed attempts. Returning to the main page.")

    def is_strong_password(self, password):
        if len(password) < 8:
            return "Password must be at least 8 characters."
        if not re.search(r'[A-Z]', password):
            return "Password must contain at least one uppercase letter."
        if not re.search(r'[a-z]', password):
            return "Password must contain at least one lowercase letter."
        if not re.search(r'\d', password):
            return "Password must contain at least one number."
        if not re.search(r'[!@#$%^&*()]', password):
            return "Password must contain at least one special character."
        return "Strong"

    def save_users(self):
        with open(self.filename, "w") as file:
            for user in self.users.values():
                file.write(json.dumps(user) + "\n")

# Define the PasswordRecovery function
def PasswordRecovery():
    manager = UserManager('register_user.txt')
    attempts = 0

    while attempts < 3:
        identifier = input("Enter your username or phone number: ").strip()

        if manager.is_user_exist(identifier):
            print("User found! You can now reset your password.")
            manager.set_password(identifier)  # Proceed to password reset
            return
        else:
            print("User not found.")
            choice = input("Would you like to [register], [retype], or [leave]? ").strip().lower()

            if choice == 'leave':
                print("You have returned to the main page.")
                return
            elif choice == 'register':
                user_register_instance = UserRegisteration()  # Create an instance of UserRegisteration
                user_register_instance.user_register()  # Call the user_register method
                return
            elif choice == 'retype':
                attempts += 1
                print(f"Remaining attempts: {3 - attempts}")
            else:
                print("Invalid choice. Please enter 'register', 'retype', or 'leave'.")

    print("Too many failed attempts. Returning to the main page.")
    print("You have returned to the main page.")

# Call PasswordRecovery function to test
PasswordRecovery()

