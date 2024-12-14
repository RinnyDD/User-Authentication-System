import sys
import os
 

# Add the modules folder to sys.path
sys.path.append(os.path.abspath(r"D:\Vs python\github user\User-Authentication-System\modules"))

# Now import the User class from base_register
from base_register import User
import json
import os
from Encrytions import encrypt_data, load_or_generate_key 


Max_Attempts = 3
Attempt = 0

class UserRegisteration(User):
    def __init__(self):
        super().__init__()
        self.user_date = {}

    def user_register(self):
        Max_Attempts = 3
        Attempt = 0

        print("\nPlease follow the instructions to register a new account.\n")

        #Condition for input Firstname and Lastname 
        while True:
            self.firstname = input("First name: ").strip()
            if len(self.firstname) < 2:
                print("First name must have at least 2 character!!!")
                continue

            self.lastname = input("Last name: ").strip()
            if len(self.lastname) < 2:
                print("First name must have at least 2 character!!!")
                continue
            break

        #Username with attempt
        while Attempt < Max_Attempts:
            self.username = input("Username: ").strip()
            if self.check_duplicate_username(self.username):
                Attempt += 1
                print("Username already taken, please choose a different one.")
                print(f"Attempts remaining: {Max_Attempts - Attempt}")
                if Attempt >= Max_Attempts:
                    print("Too many Attempts. Registeration Failed.")
                    return
            else:
                print("Username accepted!")
                break

        #Reset attempt from username input
        Attempt = 0
        #Password set up and check the condition

        while True:
            password = input("Enter your password: ").strip()
            

            strength = self.Check_Password_strength(password)
            print(f"Password strength: {strength}")

            if strength == "Weak":
                print("Error: Password is too weak. Use a stronger password.")
                continue

            elif strength == "Moderate":
                print("Error: Password is Moderate. Use a stronger password.")
                continue

            while Attempt < Max_Attempts:
                confirm_password = input("Confirm your password: ").strip()
                if password != confirm_password:
                    Attempt += 1
                    print("Error: Password does not match. Please try again.")
                    print(f"Attempts remaining: {Max_Attempts - Attempt}")
                    if Attempt >= Max_Attempts:
                        print("Too many attempts. Registration Failed.")
                        return
                else:
                    self.set_password(password)
                    print("Password set successfully!")
                    break
            if password == confirm_password:
                break

        while True:
            phone = input("Phone number: +855 ").strip()
            hone = phone.replace(" ", "")
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
            file_name = r"D:\Vs python\github user\User-Authentication-System\main\database.txt"
            if os.path.exists(file_name):
                with open(file_name, 'r') as file:
                    try:
                        data = json.load(file)  # Load existing JSON data
                    except json.JSONDecodeError:
                        data = []  # If the file is empty or corrupted, initialize an empty list

            # Check if username already exists in the loaded data
                for existing_user in data:
                    if existing_user['username'] == username:  # Case-insensitive comparison
                        return True  # Username found, duplicate exists
        
            return False  # No duplicate found
        except (OSError, json.JSONDecodeError) as e:
            print(f"Error checking duplicates: {e}")
            return False
        
    def Check_Password_strength(self, password):
        #initailized
        uppercase = any(char.isupper() for char in password)
        lowercase = any(char.islower() for char in password)
        digit = any(char.isdigit() for char in password)
        special_char = any(char in "!@#$%^&*()" for char in password)

        # Classify the password
        if len(password) >= 8 and uppercase and lowercase and digit and special_char:
            return "Strong"
        elif len(password) >= 8 and ((uppercase and lowercase and digit) or special_char):
            return "Moderate"
        else:
            return "Weak"
        
    def check_phone_number(self, phone_number):
        phone_number = phone_number.replace(" ", "")
        return phone_number.isdigit() and 8 <= len(phone_number) <= 9
        
    def save_user_data(self):

        #Use for remove all the space and phone number store like '+855 11123456'
        formatted_phone = self.phone[4:].replace(" ", "")
        Phone = "+855 " + formatted_phone
        key = load_or_generate_key()
        cipher = encrypt_data(key)
        

        user_data = {
            'firstname': self.firstname,
            'lastname': self.lastname,
            'username': self.username,
            'phone': Phone,
            'password': cipher.encrypt(self.get_password().encode()).decode()
        }

        try:
            script_directory = os.path.dirname(os.path.abspath(__file__))
            os.chdir(script_directory)
            file_name = r"D:\Vs python\github user\User-Authentication-System\main\database.txt"
            
            if os.path.exists(file_name):
                with open(file_name, "r") as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []  # If file exists but is empty or corrupted, start with an empty list
            else:
                    data = []

                # Append new user data to the list
            data.append(user_data)

                # Save the updated data back to the file
            with open(file_name, "w") as file:
                json.dump(data, file, indent=4)
                print(f"User data saved to '{file_name}'")

        except OSError as e:
                print(f"Error saving user data: {e}")


