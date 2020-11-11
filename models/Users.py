import json
from bson.json_util import loads
from config import client


class LogIn:

    def __init__(self, username, password):
        self.UserName = username
        self.Password = password

    def check_username(self):
        database = client.Parking_Users
        collection = database['Users']
        users = collection.find_one(
            {'UserName': self.UserName, 'Password': self.Password}
        )
        if users is not None:
            return True
        else:
            return False

    def return_data(self):
        db = client[f'{self.UserName}']
        collection = db[f'{self.UserName}_DATA']
        return collection.find_one()


class SingUp:
    database = client.Parking_Users
    collection = database['Users']

    def __init__(self, first_name, family_name, username,
                 password, confirm_password, email, phone):
        self.FirstName = first_name
        self.FamilyName = family_name
        self.UserName = username
        self.Password = password
        self.Confirm_Password = confirm_password
        self.Email = email
        self.Phone = phone
        self.serialize = None

    def serialize_information(self):
        data = {
            'UserName': self.UserName,
            'Password': self.Password,
            'FirstName': self.FirstName,
            'FamilyName': self.FamilyName,
            'Email': self.Email,
            'Phone': self.Phone
        }
        json_data = json.dumps(data)
        serialize = loads(json_data)
        self.serialize = serialize

    def check_information(self):
        if self.UserName.isspace() or self.Password.isspace() or \
                len(self.UserName) < 4 or len(self.Password) < 4:
            print('Your UserName And Password Should be more Than 3 Character!')
            return False
        else:
            return True

    def check_password(self):
        if self.Password == self.Confirm_Password:
            return True
        else:
            print("Your Password And Confirm Password Aren't Same!")
            return False

    def check_username(self):
        users = SingUp.collection.find()
        list_users = [u['UserName'] for u in users]
        if self.UserName in list_users:
            print('Your UserName Is Exist!')
            return False
        else:
            return True

    def insert_user_to_mongodb_users(self):
        SingUp.collection.insert_one(self.serialize)

    def create_user_database(self, parking_data):
        user_database = client[f'{self.UserName}']
        collection = user_database[f'{self.UserName}_DATA']
        collection.insert_one(parking_data)
        print('You Can Now Login.')

    def __str__(self):
        return f'Create This User:\n' \
               f'FirstName: {self.FirstName}\n' \
               f'FamilyName: {self.FamilyName}\n' \
               f'UserName: {self.UserName}\n' \
               f'Password: {self.Password}\n' \
               f'Email: {self.Email}\n' \
               f'Phone: {self.Phone}'

    def delete_user(self):
        SingUp.collection.delete_one({'UserName': self.UserName})

    def create_user(self):
        if self.check_information() and self.check_password() and self.check_username():
            self.serialize_information()
            return True
        else:
            return False
