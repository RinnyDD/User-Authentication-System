import sys
import os
 

# Add the modules folder to sys.path
sys.path.append(os.path.abspath(r"D:\Vs python\github user\User-Authentication-System\modules"))
from register_function import register_function

def main():
    while True:
        print("1. Register\n2. Login\n3. Password Recovery\n4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            register_function()

        '''elif choice == "2":
            login_system = Login()
            login_system.login()
        elif choice == "3":
            PasswordRecovery()
        
        elif choice == "4":
            break
        else:
            print("Invalid choice.")'''
