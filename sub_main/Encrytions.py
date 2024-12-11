from cryptography.fernet import Fernet


def load_or_generate_key(key_file="pw.key"):
    try:
        with open(key_file, "rb") as file:
            keyforpw = file.read()
            print("Key loaded successfully.")
            return keyforpw
    except FileNotFoundError:
        keyforpw = Fernet.generate_key()
        with open(key_file, "wb") as file:
            file.write(keyforpw)
            print("New key generated and saved.")
        return keyforpw

def encrypt_data(key):
    return Fernet(key)
        