import atexit

from Database import *
from User import Model


# Data Storing when program crush/exit
@atexit.register
def storing():
    r = root
    if r is not None:
        testList = r.store_in_DB(r)
        for i in testList:
            print(14, i.Email)
        print("Storing successfully!")


global root
root = db_getAll()


class Project:

    def __init__(self):
        if root is not None:
            self.db = root
        else:
            self.db = BST(None)
        self.user_menu()

    def user_menu(self):
        while True:
            user_input = input(f'Press 1 to insert new user\n'
                               f'Press 2 to find existing user\n'
                               f'Press 3 to login user\n'
                               f'Type "exit" to exit\n'
                               f'>> ')

            if user_input == '1':
                self.insert_user()
                break

            elif user_input == '2':
                self.find_user()
                break

            elif user_input == '3':
                self.login_user()
                break

            elif user_input == "exit":
                exit()

            else:
                print("Input Wrong. Try again!\n")

    def insert_user(self):
        while True:
            email = input("Enter your email: ")
            if email == "exit":
                exit()

            email_format = self.email_checking(email)

            # checking email format and existed in db or not
            if email_format == 1:
                pw = input("Enter your password: ")
                name = input("Enter your name: ")
                phone = input("Enter your phone number(must have 11): ")

                user: object = Model(email, pw, name, phone)

                if self.db.data is None:
                    self.db = BST(user)
                    global root
                    root = self.db
                    print("Root Inserted")

                else:
                    email_existed = self.db.find(self.db, email)
                    phone_existed = self.db.find_phone(self.db, phone)

                    print('e', email_existed)
                    print('p', phone_existed)

                    if not email_existed and phone_existed:
                        self.db.create(self.db, user)
                        print("Child Inserted\n")
                        # uList: list = self.db.get_all(self.db)
                        # for i in uList:
                        #     print("Email:", i.Email)

                    elif email_existed:
                        print("Email is already existed!\n")

                    elif phone_existed is False:
                        print("Phone is already existed!\n")

                self.other_options(user)

            else:
                print("Email format is wrong. Try again!\n")

    def find_user(self):
        while True:
            f_email = input("Enter customer's email or phone number: ")
            if f_email == "exit":
                exit()
            if self.email_checking(f_email) == -1:
                print("Email format is wrong. Try again!\n")
            else:
                user = self.db.find(self.db, f_email)
                if user:
                    print(f"_____User Info_____\n"
                          f"Name: {user.data.Name}\n"
                          f"Email: {user.data.Email}\n"
                          f"Phone: {user.data.Phone}\n")
                else:
                    print("User Not Found!")

    def login_user(self):
        while True:
            l_email = input("Enter email to login: ")
            check_user = self.db.find(self.db, l_email)

            if l_email == 'back':
                self.user_menu()
                break
            elif l_email == 'exit':
                exit()
            else:
                if self.email_checking(l_email) == 1 and check_user:
                    self.other_options(check_user.data)

                elif self.email_checking(l_email) == -1:
                    print("Email Invalid!")

                elif not check_user:
                    print("Email is not existed!")

    def other_options(self, user: object):
        while True:
            choices = input(f'Press 1 to change user info:\n'
                            f'Press 2 to delete user acc:\n'
                            f'Type "main" to go Main Menu:\n'
                            f'Type "insert" to create new user:\n'
                            f'>> ')
            if choices == '1':
                self.update_user(user)

            elif choices == '2':
                self.del_user(user)

            elif choices == 'main':
                self.user_menu()
                break

            elif choices == 'insert':
                self.insert_user()
                break

            else:
                print("Invalid Option!")

    def update_user(self, user: object):
        while True:
            print(f"_____Update Section_____\n"
                  f"Skip input if you don't want to change:")
            u_email = input("Enter new email:")
            u_pw = input("Enter new password: ")
            u_name = input("Enter new name: ")
            u_phone = input("Enter new phone number(must have 11): ")

            if u_email == '':
                u_email = user.Email
                format_email = 1
            else:
                format_email = self.email_checking(u_email)

            check_phone = self.db.find_phone(self.db, u_phone)  # True
            check_email = self.db.find(self.db, u_email)

            print(format_email, check_email, check_phone)

            if u_pw == '':
                u_pw = user.Password
            if u_name == '':
                u_name = user.Name
            if u_phone == '':
                u_phone = user.Phone

            if format_email == 1 and check_email is None and check_phone:
                data = Model(u_email, u_pw, u_name, u_phone)
                print('[193]', self.db.update(self.db, user.Email, data))
                print("Updated Successfully")
                break

            elif format_email == 1 and check_phone:
                data = Model(u_email, u_pw, u_name, u_phone)
                self.db.update(self.db, u_email, data)
                break

            elif format_email == -1:
                print("Email Invalid!")

            elif check_email:
                print("[196] Email is already existed!")

            elif not check_phone:
                print("[199] Phone is already existed!")

    def del_user(self, user: object):
        self.db.delete(self.db, user.Email)
        print('Deletion successfully')

    # This is Email Format Checking Section
    def email_checking(self, r_email: str):
        name_counter = 0
        for i in range(len(r_email)):
            if r_email[i] == '@':
                # print("Name End Here")
                break
            name_counter += 1

        email_name = r_email[0:name_counter]
        email_form = r_email[name_counter:]

        # checking for name
        name_flag = 0
        email_flag = 0
        for i in range(len(email_name)):
            aChar = email_name[i]
            if (31 < ord(aChar) < 48) or (57 < ord(aChar) < 65) or (
                    90 < ord(aChar) < 97) or (122 < ord(aChar) < 128):
                name_flag = -1
                break

        domain_form = ["@facebook.com", "@ncc.com", "@mail.ru", "@yahoo.com", "@outlook.com", "@apple.com", "@zoho.com",
                       "@gmail.com"]

        for i in range(len(domain_form)):
            if domain_form[i] == email_form:
                email_flag = 1
                break

        if name_flag == -1 or email_flag == 0:
            return -1

        else:
            return 1


if __name__ == '__main__':
    p = Project()
