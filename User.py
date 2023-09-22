class Model:
    def __init__(self, email, password, name, phone):
        self.__email = email
        self.__password = password
        self.__name = name
        self.__phone = phone

    @property
    def Email(self):
        return self.__email

    @Email.setter
    def Email(self, value):
        self.__email = value

    @property
    def Password(self):
        return self.__password
    
    @Password.setter
    def Password(self, value):
        self.__password = value
    
    @property
    def Name(self):
        return self.__name
    
    @Name.setter
    def Name(self, value):
        self.__name = value
    
    @property
    def Phone(self):
        return self.__phone
    
    @Phone.setter
    def Phone(self, value):
        self.__phone = value
