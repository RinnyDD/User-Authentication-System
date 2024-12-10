import random
import maskpass
import os
import hashlib
import time
COOLDOWN_TIME_LOGIN = 60
COOLDOWN_TIME_CODE = 30

class Login:
    def __init__(self, database="user_data.txt"):
        self.database = database

    # Helper function to hash passwords
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    # Verify username and password
    def verify(self, username, password):
        if not os.path.exists(self.database):
            print("Error: User data file not found.")
            return False

        try:
            with open(self.database, "r") as file:
                users = {}
                for line in file:
                    stored_username, stored_password = line.strip().split(",")
                    users[stored_username] = stored_password
        except Exception as e:
            print(f"Error reading user data: {e}")
            return False

        # Check if the username exists
        if username not in users:
            print("!!! Invalid username !!!")
            return "username_invalid"

        # Hash the entered password and compare it with the stored hash
        entered_hashed_password = self.hash_password(password)
        if entered_hashed_password != users[username]:
            return "password_invalid"

        # If both username and password match
        return True

    # Generate a random code
    def generate_random_code(self, length=6, codes=''):
        characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890123456789'
        
        return ''.join(random.choice(characters) for _ in range(length))

def main():
    MAX_ATTEMPTS = 3
    login_system = Login()
    print("Welcome to the Login System!")

    while True:
        # Prompt for username
        while True:
            username = input("Enter username: ").strip()
            verification_result = login_system.verify(username, "")
            if verification_result == "username_invalid":
                print("Please try again.")
            else:
                break
        attempts_login = 0
        attempts_code = 0
        # Prompt for password
        while attempts_login < MAX_ATTEMPTS:
            password = maskpass.askpass(mask='-').strip()
            verification_result = login_system.verify(username, password)
            if verification_result == "password_invalid":
                print("!!!  Wrong password  !!!")
                print("!!! Please try again !!!")
                
            elif verification_result is True:
                code = login_system.generate_random_code()
                print("Your verification code is:{}".format(code))
                verify_code = input("Enter code: ")
                if verify_code != code:
                    print("!!! Wrong code !!!")
                while verify_code != code:
                    
                    choices = input("Do you want to [retype] or [resend] the code ? --> ").strip().lower()
                            
                    if choices =='resend' or choices == 'rs':
                        code = login_system.generate_random_code()
                        print("Your verification code is:{}".format(code))
                        verify_code = input("Enter code: ").strip()
                        if verify_code != code:
                            print("Please wait before sending again.")
                            for remaining_time in range(COOLDOWN_TIME_CODE, 0, -1):
                                print(f"Cooldown time remaining: {remaining_time} seconds", end="\r")
                                time.sleep(1)
                            continue
                        if verify_code == code:
                            print("You have successfully logged in to your account!")
                            break
                           
                        if verify_code != code:
                            print("!!! Wrong code !!!")
                            
                    elif choices =='retype' or choices == 'rt':
                     
                        while verify_code != code and attempts_code < MAX_ATTEMPTS:
                            verify_code = input("Enter code again: ").strip()
                            attempts_code += 1
                            print(f"Remaining attempts: {MAX_ATTEMPTS - attempts_code}")
                            print("Too many failed attempts. Access denied.")
                        if verify_code == code:
                            print("You have successfully logged in to your account!")
                        break
                    
                    else:
                        print("Invalid choice! Please choose the correct choice.")
                    
                return
            else:
                break  # Unexpected error
            attempts_login += 1
            print(f"Remaining attempts: {MAX_ATTEMPTS - attempts_login}")
        print("Too many failed attempts. Access denied.")
        if attempts_login >= MAX_ATTEMPTS:
            print("Too many failed attempts. Please wait before trying again.")
            for remaining_time in range(COOLDOWN_TIME_LOGIN, 0, -1):
                print(f"Cooldown time remaining: {remaining_time} seconds", end="\r")
                time.sleep(1)
            return

if __name__ == "__main__":
    main()

