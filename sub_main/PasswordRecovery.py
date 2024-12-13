import os
import json
import re

class UserManager:
    def __init__(self, filename="register_user.txt"):
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
        print("You have returned to the main page.")

    def is_strong_password(self, password):
        # Ensure the password is at least 8 characters long
        if len(password) < 8:
            return False

        # Regular expressions to check for required character types
        if not re.search(r'[A-Z]', password):  # At least one uppercase letter
            return False
        if not re.search(r'[a-z]', password):  # At least one lowercase letter
            return False
        if not re.search(r'\d', password):     # At least one digit
            return False
        if not re.search(r'[!@#$%^&*()]', password):  # At least one special character
            return False

        return True

    def save_users(self):
        with open(self.filename, "w") as file:
            for user in self.users.values():
                file.write(json.dumps(user) + "\n")

def register():
    manager = UserManager('register_user.txt')

    # Collect user details
    first_name = input("Enter your first name: ").strip()
    last_name = input("Enter your last name: ").strip()
    
    # Username input and check for duplicates
    while True:
        username = input("Enter a username: ").strip()
        if manager.is_user_exist(username):
            print("Username already exists. Please choose a different username.")
        else:
            break

    # Phone number input and validation
    while True:
        phone = input("Enter your phone number: ").strip()
        if not phone.isdigit():
            print("Invalid phone number. Please enter numbers only.")
        elif manager.is_user_exist(phone):
            print("Phone number already exists. Please use a different phone number.")
        else:
            break

    # Prompt user to set a strong password
    attempts = 0
    while attempts < 3:
        password = input("Enter a strong password: ").strip()
        if manager.is_strong_password(password):
            confirm_password = input("Confirm your password: ").strip()
            if password == confirm_password:
                # Save the user data if everything is correct
                user_data = {
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone": phone,
                    "password": password
                }
                manager.users[username] = user_data
                manager.save_users()
                print("Registration successful!")
                return
            else:
                print("Error: Passwords do not match. Please try again.")
        else:
            print("Password is not strong enough. Use a combination of uppercase, lowercase, numbers, and special characters.")
        
        attempts += 1
        print(f"Remaining attempts: {3 - attempts}")

    print("Too many failed attempts. Registration aborted.")
    print("You have returned to the main page.")

def PasswordRecovery():
    manager = UserManager('register_user.txt')
    attempts = 0

    while attempts < 3:
        identifier = input("Enter your username or phone number: ").strip()

        if manager.is_user_exist(identifier):
            print("User found! You can now reset your password.")
            manager.set_password(identifier)
            return
        else:
            print("User not found.")
            choice = input("Would you like to [register], [retype], or [leave]? ").strip().lower()

            if choice == 'leave':
                print("You have returned to the main page.")
                return
            elif choice == 'register':
                register()
                return
            elif choice == 'retype':
                attempts += 1
                print(f"Remaining attempts: {3 - attempts}")
            else:
                print("Invalid choice. Please enter 'register', 'retype', or 'leave'.")

    print("Too many failed attempts. Returning to the main page.")
    print("You have returned to the main page.")

# Run PasswordRecovery function to test
PasswordRecovery()
