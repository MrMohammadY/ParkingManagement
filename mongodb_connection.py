import pymongo
from config import password

client = pymongo.MongoClient(f"mongodb+srv://MMD:{password}"
                             f"@parkingmanagementcluste.kihxb.mongodb.net/"
                             f"<dbname>?retryWrites=true&w=majority")


def connect_to_specific_database(username):
    db = client[f'{username}']
    collection = db[f'{username}_DATA']
    return collection.find_one()


def log_in_check_exist_username(username, pass_word):
    db = client.Parking_Users
    collection = db['Users']
    users = collection.find_one({'username': username, 'password': pass_word})
    if users is not None:
        return connect_to_specific_database(username)
    else:
        print('Your Username Or Password Incorrect!')
        return False


def sing_up_check_users(username, pass_word, confirm_password):
    db = client.Parking_Users
    collection = db['Users']
    users = collection.find()
    list_users = [u['username'] for u in users]

    if username not in list_users:
        if pass_word == confirm_password:
            data = {'username': username, 'password': pass_word}
            collection.insert_one(data)
            print('Create User')
            return True
        else:
            print('Password is not correct!')
            return False
    else:
        print('Username is exist!')
        return False


def create_database_user(username, data):
    new_db = client[f'{username}']
    collection = new_db[f'{username}_DATA']
    collection.insert_one(data)
