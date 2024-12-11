import random
import maskpass
import os
import time

COOLDOWN_TIME_LOGIN = 60
COOLDOWN_TIME_CODE = 30
MAX_ATTEMPTS = 3

class Login:
    def __init__(self, database="register_user.txt"):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.database = os.path.join(script_directory, database)

    
    # Verify username and password
    def verify(self, username, password):
        
        if not os.path.exists(self.database):
            print("Error: User data file not found.")
            return False

        try:
            script_directory = os.path.dirname(os.path.abspath(__file__))
            os.chdir(script_directory)
            
            with open(self.database, "r") as file:
                users = {}
                
                for line in file:
                    user_data = eval(line.strip())
                    user_data = eval(line.strip())
                    check_username = user_data.get("username")
                    check_password = user_data.get("password")
                    
                    if check_username and check_password:
                        users[check_username] = check_password
                        
        except Exception as e:
            print(f"Error reading user data: {e}")
            return False

        # Check if the username exists
        if username not in users:
            print("!!! Invalid username !!!")
            return "username_invalid"

        if password != users[username]:
            return "password_invalid"
        return True

    #Generate a random code
    def generate_random_code(self, length = 6):
        characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890123456789'
        return ''.join(random.choice(characters) for _ in range(length))

    def login(self):
        print("Welcome to the Login System!")
        
        while True:
            # Prompt for username
            while True:
                username = input("Enter username: ").strip()
                verification_result = self.verify(username, "")
                
                if verification_result == "username_invalid":
                    print("Please try again.")
                    
                else:
                    break
            
            attempts_login = 0
            
            # Prompt for password
            while attempts_login < MAX_ATTEMPTS:
                password = maskpass.askpass(mask='').strip()
                verification_result = self.verify(username, password)
                
                if verification_result == "password_invalid":
                    print("!!! Wrong password !!!")
                    print("!!! Please try again !!!")
                    
                elif verification_result is True:
                    self.verify_code_flow()
                    return
                
                else:
                    break  # Unexpected error
                
                attempts_login += 1
                print(f"Remaining attempts: {MAX_ATTEMPTS - attempts_login}")
            print("Too many failed attempts. Access denied.")
            if attempts_login >= MAX_ATTEMPTS:
                print("Please wait before trying again.")
                
                for remaining_time in range(COOLDOWN_TIME_LOGIN, 0, -1):
                    print(f"Cooldown time remaining: {remaining_time} seconds", end="\r")
                    time.sleep(1)
                return

    def verify_code_flow(self):
        code = self.generate_random_code()
        print("Your verification code is:{}".format(code))
        attempts_code_retype = 0
        attempts_code_resend = 0
        
        while attempts_code_resend < MAX_ATTEMPTS or attempts_code_retype < MAX_ATTEMPTS:
            verify_code = input("Enter code: ").strip().upper()
            
            if verify_code == code:
                print("You have successfully logged in to your account!")
                break
            
            if verify_code != code:
                    print("!!! Wrong code !!!")
                    
            while verify_code != code:
                choices = input("Do you want to [retype], [resend] or [leave] the code ? --> ").strip().lower()
        
                if choices =='resend' or choices == 'rs':
                    code = self.generate_random_code()
                    print("Your verification code is:{}".format(code))
                    verify_code = input("Enter code: ").strip().upper()
                    attempts_code_retype = 0    
                    if verify_code != code:
                        if attempts_code_resend == MAX_ATTEMPTS - 1:
                            print("Too many wrong code, you cannot login to your account.")
                            print("Try again next time, Good luck !")
                            break   
                        print("Please wait before trying again.")
                        attempts_code_resend += 1
                        print(f"Remaining attempts: {MAX_ATTEMPTS - attempts_code_resend}")
                        print("Too many failed attempts. Access denied.")
                        
                        
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
                    
                    if verify_code != code and attempts_code_retype < MAX_ATTEMPTS:
                        verify_code = input("Enter code again: ").strip().upper()
                        
                        if verify_code != code:
                            attempts_code_retype += 1
                            print(f"Remaining attempts: {MAX_ATTEMPTS - attempts_code_retype}")
                            print("Too many failed attempts. Access denied.")
                                 
                        
                        elif verify_code == code:
                            print("You have successfully logged in to your account!")
                            
                        else:
                            break
                    
                    elif attempts_code_retype == 3:
                        print("Too many wrong code, you can't login to your account.")
                        print("Please resend the code and try again !")
    
                elif choices == 'leave' or choices == 'l':
                    print("Thank you for using my service, Have a good day ! ")
                    break
                else:
                    print("Invalid choice! Please choose the correct choice.")
                    
            return

# Create an instance of the Login class and call the login process
login_system = Login()
login_system.login()
