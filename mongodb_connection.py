import pymongo
from config import mongodb_password

# connection with mongodb and save our link into client
# client = pymongo.MongoClient(f"mongodb+srv://MMD:{mongodb_password}"
#                              f"@parkingmanagementcluste.kihxb.mongodb.net/"
#                              f"<dbname>?retryWrites=true&w=majority")

client = pymongo.MongoClient(f"mongodb+srv://Hossein:{mongodb_password}"
                             f"@cluster0.y9iwi.mongodb.net/"
                             f"<dbname>?retryWrites=true&w=majority")

# connect to our parking users database.

parking_users_db = client.Parking_Users

# choose Users collection.
users_collection = parking_users_db['Users']


def is_this_user_exist(username, password):
    """
    check and authentication this user exist in our system or not base on his username and password.
    :param username: parking username
    :param password: parking password
    :return: True if this user exist in our system and
             False if this user doesn't exist.
    """

    # find out this user
    user = users_collection.find_one({'username': username, 'password': password})

    # check user exist or not
    if user is not None:
        return True
    return False


def connect_to_specific_database(username):
    """
    connect to a specific parking database base on its username.
    :param username: parking username.
    :return: a particular parking database.
    """

    db = client[f'{username}']
    return db


def sign_up_users(username, password, confirm_password):
    """
    a method for check user sign up process and add this user to our system.
    :param username: new parking username
    :param password: new parking password
    :param confirm_password: new parking confirm password.
    :return: True if this process completely done without any problems and
             False if some problems occur in this process.
    """

    # by default we considering this user doesn't created and
    # if user created change this situation.
    can_create_new_user = False

    # check this username already exist or not
    if not(is_this_user_exist(username, password)):

        # check user password and confirm password are same.
        if password == confirm_password:

            # if everything is ok, add this user to our system.
            user_data = {'username': username, 'password': password}
            users_collection.insert_one(user_data)

            print('@' * 60)
            print('Create This User')
            print('@' * 60)

            # change default situation.
            can_create_new_user = True
            return can_create_new_user

        else:
            # if password and confirm password aren't same.
            print('@' * 60)
            print('password and confirm password are not same!')
            print('@' * 60)
            return can_create_new_user
    else:
        # if this username already exist.
        print('@' * 60)
        print('This username is already exist and taken by another users!')
        print('@' * 60)
        return can_create_new_user


def create_particular_database_for_each_parking(username, data):
    new_parking_db = client[f'{username}']
    new_parking_collection = new_parking_db[f'{username}_DATA']
    new_parking_collection.insert_one(data)
