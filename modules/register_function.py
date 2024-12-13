import sys
import os
 
# Add the modules folder to sys.path
sys.path.append(os.path.abspath(r"D:\Vs python\github user\User-Authentication-System\sub_main"))
from Register import UserRegisteration
def register_function():
    user_registeration = UserRegisteration()
    user_registeration.user_register()
    print("\nRegistration Complete!")
    print("Thank you for joining our system!\n")
    print("="*50)
    print("\n")
