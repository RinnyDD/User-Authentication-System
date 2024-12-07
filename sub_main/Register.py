import os
import json
class User:
    def __init__(self, firstname = None, lastname = None, username = None, phone = None, password = None):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.phone = phone
        self.__password = password

    def set_password(self, password):
        self.__password = password

    def get_password(self):
        return self.__password

class UserRegisteration(User):
    def __init__(self):
        super().__init__()
        self.user_date = {}

    def user_register(self):
        self.firstname = input("First name: ").strip()
        self.lastname = input("Last name: ").strip()

        while True:
            self.username = input("Username: ").strip()
            if self.check_duplicate_username(self.username):
                print("Username already taken, please choose a different one.")
            else:
                break
        
        while True:
            password = input("Enter your password: ").strip()
            confirm_password = input("Confirm your password: ").strip()

            if password != confirm_password:
                print("Error: Password does not match. Please try again.")
                continue

            strength = self.Check_Password_strength(password)
            print(f"Password strength: {strength}")

            if strength == "Weak":
                print("Error: Password is too weak. Use a stronger password.")
                
            elif strength == "Moderate":
                print("Error: Password is Moderate. Use a stronger password.")
            
            else:
                self.set_password(password)
                break

        while True:
            phone = input("Phone number: +855 ").strip()
            if self.check_phone_number(phone):
                self.phone = "+855 " + phone
                break
            print("Error: Invalid phone number. Please enter 8–9 digits after +855.")

        self.save_user_data()
        print("Registered Successfully!")

    def check_duplicate_username(self, username):
        try:
            script_directory = os.path.dirname(os.path.abspath(__file__))
            os.chdir(script_directory)
            file_name = "register_user.txt"
            if os.path.exists(file_name):
                with open(file_name , 'r') as file:
                    for line in file:
                        existing_user = eval(line.strip())
                        if existing_user['username'] == username:
                            return True 
            return False
        except (OSError, SyntaxError) as e:
            print(f"Error checking duplicates: {e}")
            return False
        
    def Check_Password_strength(self, password):
        #initailized
        uppercase = any(char.isupper() for char in password)
        lowercase = any(char.islower() for char in password)
        digit = any(char.isdigit() for char in password)
        special_char = any(char in "!@#$%^&*()" for char in password)

        # Classify the password
        if len(password) >= 12 and uppercase and lowercase and digit and special_char:
            return "Strong"
        elif len(password) >= 8 and ((uppercase and lowercase and digit) or special_char):
            return "Moderate"
        else:
            return "Weak"
        
    def check_phone_number(self, phone_number):

        return phone_number.isdigit() and 8 <= len(phone_number) <= 9
        
    def save_user_data(self):
        user_data = {
            'firstname': self.firstname,
            'lastname': self.lastname,
            'username': self.username,
            'phone': self.phone,
            'password': self.get_password()
        }

        try:
            script_directory = os.path.dirname(os.path.abspath(__file__))
            os.chdir(script_directory)
            file_name = "register_user.txt"
            if not os.path.exists(file_name):
                with open(file_name, "w") as file:
                    file.write(str(user_data) + "\n")
                print(f"File '{file_name}' created and user data saved.")
            else:
                with open(file_name, "a") as file:
                    file.write(str(user_data) + "\n")
                print(f"User data appended to '{file_name}'.")
        except OSError as e:
            print(f"Error saving user data: {e}")

user_registeration = UserRegisteration()
user_registeration.user_register()
