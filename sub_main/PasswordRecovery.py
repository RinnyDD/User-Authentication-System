import re

class UserManager:
    def __init__(self, file_name):
        self.file_name = file_name
        self.users = self.load_users()

    def load_users(self):
        """Load users from the file into a dictionary."""
        try:
            with open(self.file_name, 'r') as file:
                users = {}
                for line in file:
                    username, phone, password = line.strip().split(',')
                    users[username] = {'phone': phone, 'password': password}
                return users
        except FileNotFoundError:
            print(f"{self.file_name} not found. Please create the file or check the path.")
            return {}

    def save_users(self):
        """Save updated users back to the file."""
        with open(self.file_name, 'w') as file:
            for username, data in self.users.items():
                file.write(f"{username},{data['phone']},{data['password']}\n")

    def is_user_exist(self, identifier):
        """Check if a user exists by username or phone."""
        return any(identifier in (username, data['phone']) for username, data in self.users.items())

    def set_password(self, identifier):
        """Allow the user to set a new password if the identifier is found."""
        new_password = input("Enter a new password: ")
        if self.is_strong_password(new_password):
            for username, data in self.users.items():
                if identifier in (username, data['phone']):
                    self.users[username]['password'] = new_password
                    self.save_users()
                    print("Password updated successfully!")
                    return
        else:
            print("Password is not strong enough. Please try again.")

    @staticmethod
    def is_strong_password(password):
        """Check if a password is strong."""
        if len(password) < 8 or not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password) or not re.search(r'\d', password):
            return False
        if not re.search(r'[@$!%*?&#]', password):
            return False
        return True

    def register_user(self):
        """Register a new user if they do not already exist."""
        username = input("Enter a username: ")
        phone = input("Enter a phone number: ")
        if self.is_user_exist(username) or self.is_user_exist(phone):
            print("User already exists.")
        else:
            password = input("Enter a password: ")
            if self.is_strong_password(password):
                self.users[username] = {'phone': phone, 'password': password}
                self.save_users()
                print("Registration successful!")
            else:
                print("Password is not strong enough. Registration failed.")

def main():
    manager = UserManager('usersecrect.txt')
    identifier = input("Enter your username or phone number: ")

    if manager.is_user_exist(identifier):
        manager.set_password(identifier)
    else:
        print("User not found. Would you like to register?")
        choice = input("Enter 'yes' to register or 'no' to exit: ").lower()
        if choice == 'yes':
            manager.register_user()
        else:
            print("Goodbye!")

if __name__ == "__main__":
    main()

