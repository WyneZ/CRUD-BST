from User import Model
import mysql.connector

# secondary db
db_connection = mysql.connector.connect(
    host="localhost",
    user="wk",
    password="wynekyaw",
    auth_plugin="mysql_native_password",
    database="testDB1",
)

db_create = '''CREATE TABLE Users (
             Id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
             Name varchar(255),
             Email varchar(255),
             Password varchar(255),
             Phone varchar(255)
             )'''

db_cursor = db_connection.cursor()


# db_cursor.execute(db_create)


def db_insert(dataList: list):
    for user in dataList:
        data = (user.Name, user.Email, user.Password, user.Phone)
        db_cursor.execute("insert into testDB1.Users (Name, Email, Password, Phone) values (%s, %s, %s, %s)", data)
        db_connection.commit()
    return dataList


def db_getAll():
    root = None
    try:
        db_cursor.execute("select * from Users")
        objList = []
        for data in db_cursor:
            print(data)
            obj = Model(data[2], data[3], data[1], data[4])
            objList.append(obj)
        i = 0
        for a in objList:
            if i == 0:
                root = BST(a)
                i = 1
            else:
                root.create(root, a)
        db_delAll()
        db_connection.commit()
        return root
    except:
        return False

    # root.display(root)


def db_delAll():
    db_cursor.execute("delete from Users")
    db_connection.commit()


class BST:
    def __init__(self, data: object):
        self.data = data
        self.left = None
        self.right = None
        self.storeList: list = []
        self.responseList: list = []
        # db_getAll()

    def create(self, node: object, data: object):
        if node is None:
            new_node: BST = BST(data)
            return new_node
        elif data.Email < node.data.Email:
            node.left = self.create(node.left, data)
        elif data.Email > node.data.Email:
            node.right = self.create(node.right, data)
        return node

    def display(self, node: object):
        if node:
            self.display(node.left)
            self.responseList.append(node.data)
            self.display(node.right)

    def find(self, root: object, data: str):  # read
        if root is None or root.data.Email == data:
            return root
        if data < root.data.Email:
            return self.find(root.left, data)
        else:
            return self.find(root.right, data)

    def find_phone(self, root: object, phone: str):
        self.display(root)
        for i in self.responseList:
            if i.Phone == phone:
                return False
            else:
                return True

    def update(self, root: object, target: str, data: object):
        if root is None or root.data.Email == target:
            root.data = data
            return root
        if target < root.data.Email:
            return self.update(root.left, target, data)
        else:
            return self.update(root.right, target, data)

    def delete(self, root: object, data: str):
        if root is None:
            return root

        if data < root.data.Email:
            root.left = self.delete(root.left, data)

        elif data > root.data.Email:
            root.right = self.delete(root.right, data)

        elif data == root.data.Email:
            if root.left is None and root.right is None:
                root = None
                return root

            elif root.left is None:
                root = root.right

            elif root.right is None:
                root = root.left

            else:
                current = root.right
                while current.left:
                    current = current.left

                root.data = current.data
                root.right = self.delete(root.right, root.data.Email)

        return root

    def get_all(self, node: object):
        self.responseList = []
        self.display(node)
        return self.responseList

    def pre_order(self, root: object):
        if root:
            self.storeList.append(root.data)
            self.pre_order(root.left)
            self.pre_order(root.right)

    def store_in_DB(self, root: object):
        self.storeList = []
        db_delAll()
        self.pre_order(root)
        return db_insert(self.storeList)


if __name__ == "__main__":
    db_getAll()
    # obj1 = Model("w@gmail.com", "w", "W", "1234567890")
    # obj6 = Model("b@gmail.com", "b", "B", "1234567890")
    # obj2 = Model("a@gmail.com", "a", "A", "1234567890")
    # obj3 = Model("z@gmail.com", "z", "Z", "1234567890")
    # obj4 = Model("g@gmail.com", "g", "G", "1234567890")
    # obj5 = Model("j@gmail.com", "j", "J", "1234567890")

    # root_node = BST(obj1)
    # root_node.create(root_node, obj6)
    # root_node.create(root_node, obj2)
    # root_node.create(root_node, obj3)
    # root_node.create(root_node, obj4)
    # root_node.create(root_node, obj5)

    # updated_obj = Model("update@gmail.com", "UP", "UP", "00000")
    # print(root_node.update(root_node, obj2.Email, updated_obj)+"\n")
    # print(root_node.find(root_node, "j@gmail.com"))

    # print(121, root_node.delete(root_node, "a@gmail.com"))

    # root_node.delete(root_node, "z@gmail.com")
    # root_node.store_in_db(root_node)
    # print(root_node.storeList[1].Email)
    # print("Deleted:", root_node.display(root_node))
