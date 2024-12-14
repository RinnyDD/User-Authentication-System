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
