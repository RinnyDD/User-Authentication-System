import sys
import os
 

# Add the modules folder to sys.path
sys.path.append(os.path.abspath(r"D:\Vs python\github user\User-Authentication-System\modules"))
from ..sub_main import Login


login_system = Login()
login_system.login()

