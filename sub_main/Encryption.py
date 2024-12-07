from cryptography.fernet import Fernet
import ast

def load_or_generate_key(key_file="key.key"):
    try:
        with open(key_file, "rb") as file:
            print("Key loaded successfully.")
            return file.read()
    except FileNotFoundError as e:
        print(e)
    

def encrypt_data(file_path, key):
    cipher = Fernet(key)
    try:
        with open(file_path, "r") as file:
            data = ast.literal_eval(file.read())  
        print(f"Data before encryption: {data}")
        data["username"] = cipher.encrypt(data["username"].encode()).decode()
        with open(file_path, "w") as file:
            file.write(str(data))
        print("Value encrypted and saved successfully!")
    except Exception as e:
        print(f"Error during encryption: {e}")

def decrypt_data(file_path, key):
    cipher = Fernet(key)
    try:
        with open(file_path, "r") as file:
            data = ast.literal_eval(file.read())  
        print(f"Data before decryption: {data}")
        data["username"] = cipher.decrypt(data["username"].encode()).decode()
        with open(file_path, "w") as file:
            file.write(str(data))
        print("Value decrypted and saved successfully!")
        print(f"Decrypted Data: {data}")
    except Exception as e:
        print(f"Error during decryption: {e}")

# Main program
key = load_or_generate_key()
file_path = "register_user.txt"
encrypt_data(file_path, key)  
