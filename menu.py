import json
from models import Car, Factor, Park
from mongodb_connection import sign_up_users
from mongodb_connection import create_particular_database_for_each_parking
from mongodb_connection import connect_to_specific_database
from mongodb_connection import is_this_user_exist
from bson.json_util import loads
from datetime import datetime


def are_you_confirm_these_data(data, data_from):
    """
    a method to check users assurance
    :param data: this data should to check
    :param data_from: this is represent location of this date
    :return: True if user sure about his/her data and
             False if user doesn't sure.
    """

    # decorate out put such as menu
    print('!' * 60)
    print(f'!\tYou enter these data for {data_from}')
    print(f'!{data}\n')

    # get user assurance
    is_confirm = input('! Are you Confirm these data?(y/n)').strip()

    print('!' * 60)

    # check user assurance.
    if is_confirm in ('Y', 'y'):
        return True
    return False


def create_parking_object(parking_dataset_data):
    """
    this method create new object of Park class base on mongodb

    :param parking_dataset_data: get parking_DATA dataset and
                    write some attrs for new parking object

    :return: created object of Park class base on mongodb dataset information.
    """

    # create sample object of Park class
    parking = Park(parking_dataset_data['parking_name'],
                   parking_dataset_data['parking_address'],
                   parking_dataset_data['parking_capacity'],
                   parking_dataset_data['price_per_minute'])

    parking.park_place = parking_dataset_data['park_place']

    return parking


def create_factor_object(factor_dataset_data, parking, car):
    """
    this method create new object of Factor class base on mongodb

    :param factor_dataset_data: get parking_FACTOR dataset and
                    write some attrs for new factor object

    :param parking: get already parking existed object and
    :param car: get already car existed object
    :return: created object of Factor class base on mongodb dataset information.
    """

    # create a factor base on parking and a car
    sample_factor = Factor(parking, car)

    # convert datetime_in as string to python datetime object.
    car_date_time_check_in = datetime.strptime(factor_dataset_data['datetime_in'], '%Y-%m-%d %H:%M:%S.%f')

    # create factor attributes
    sample_factor.datetime_in = car_date_time_check_in
    sample_factor.car_plaque = factor_dataset_data['car_plaque']
    sample_factor.total_time_exist_in_parking = factor_dataset_data['total_time_exist_in_parking']
    sample_factor.position_park = factor_dataset_data['position_park']

    return sample_factor


def check_in_new_car(parking_db, username):
    """
    this method for check in new car into a particular parking
    :param parking_db: access to particular parking database
    :param username: particular parking username
    :return: check in new car if this process completely done without any problem and
             if some problems fall in this process back users to previous menu.
    """

    # access to parking_DATA dataset
    parking_data_dataset = parking_db[f'{username}_DATA']

    # access to parking_DATA dataset data
    parking_data_dataset_data = parking_data_dataset.find_one()

    # create parking object based on our data on mongodb
    temp_parking = create_parking_object(parking_data_dataset_data)

    # check if this parking is full or not.
    if not (temp_parking.is_full()):
        # if this parking has free space,
        # parking's employee should enter a new car plaque
        print("@" * 60)
        car_plaque = input('@ Please Enter Your Car Plaque: ').strip()
        print("@" * 60)

        # check sure about this car plaque or not
        if are_you_confirm_these_data(car_plaque, 'car plaque'):

            # create new car object.
            temp_car = Car(car_plaque)

            # create new factor object.
            temp_factor = Factor(temp_parking, temp_car)

            # access to parking_FACTOR dataset.
            parking_factor_dataset = parking_db[f'{username}_FACTOR']

            # convert python object to json from.
            temp_factor_json_form = json.dumps(temp_factor.__dict__())

            # convert above json to bson form.
            temp_factor_bson_form = loads(temp_factor_json_form)

            # insert above bson form to mongodb.
            parking_factor_dataset.insert_one(temp_factor_bson_form)

            print('#' * 60)
            print(temp_parking.park_place)
            print('#' * 60)

            # update parking free spaces after each car check in.
            parking_data_dataset.update_one({}, {'$set': {'park_place': temp_parking.park_place}})

            # return to previous menu
            return parking_menu(username)

        # if employee want to change that plaque number
        return check_in_new_car(parking_db, username)

    # if parking is completely full
    print('!' * 60)
    print('!\tParking is completely full!')
    print('!' * 60)

    # back employee to previous menu.
    return parking_menu(username)


def check_out_existed_car(parking_db, username):
    """
    this method for check out existed car from a particular parking
    :param parking_db: access to particular parking database
    :param username: particular parking username
    :return: check out exist car if this process completely done without any problem and
                 if some problems fall in this process back users to previous menu.
    """

    # access to parking_DATA dataset
    parking_data_dataset = parking_db[f'{username}_DATA']

    # access to parking_DATA dataset data
    parking_data_dataset_data = parking_data_dataset.find_one()

    # create parking object based on our data on mongodb
    temp_parking = create_parking_object(parking_data_dataset_data)

    # parking's employee should enter an existed car plaque to checkout that.
    print("@" * 60)
    car_plaque = input('@ Please Enter Your Car Plaque: ').strip()
    print("@" * 60)

    # check sure about this car plaque or not
    if are_you_confirm_these_data(car_plaque, 'car plaque'):

        # create new car object.
        temp_car = Car(car_plaque)

        # access to parking_FACTOR dataset.
        parking_factor_dataset = parking_db[f'{username}_FACTOR']

        # find this plaque in our parking_FACTOR dataset.
        result_of_search_plaque = parking_factor_dataset.find_one({'$and': [{'car_plaque': car_plaque}, {'is_out': False}]})

        # check if that plaque in our parking to find out exist or not.
        if result_of_search_plaque:
            # if exist convert bson data from mongodb to python object

            # create factor object.
            temp_factor = create_factor_object(result_of_search_plaque, temp_parking, temp_car)

            # car check out.
            # so we should express its factor.
            temp_factor.check_out()

            # represent car factor
            print('$' * 60)
            print(temp_factor)
            print('$' * 60)

            # update parking free spaces after each car check out
            parking_data_dataset.update_one({}, {'$set': {'park_place': temp_parking.park_place}})

            # update this factor after car check out
            # change is_out atr to True to show this car exited.
            parking_factor_dataset.update_one({'$and': [{'car_plaque': car_plaque}, {'is_out': False}]},
                                              {'$set': {'is_out': True}})

            return parking_menu(username)

        # if that enter plaque doesn't exist in parking.
        print('This Plaque is nit exist!')
        return check_out_existed_car(parking_db, username)

    # employee doesn't sure about car plaque and decide to change it.
    print('so, you are not sure about your enter')
    return check_out_existed_car(parking_db, username)


def parking_menu(username):
    """
    this method represent a particular parking menu after user successfully logged in
    :param username: get username from previous menu and
                     connect particular db

    :return: transfer user to check in menu or checkout menu
    """

    # connect to particular parking database base on its username.
    particular_parking_db = connect_to_specific_database(username)

    # decorate parking menu
    print(f'{"*" * 60}\n'
          f'*\t{username} Welcome To Your Panel \n'
          f'* 1. Check in new car \n'
          f'* 2. Check out existed car \n'
          f'{"*" * 60}')

    # get user choice from above menu's options
    user_choice = input('Please Choose Your Choice: ')

    # employee in parking decide to register new car and
    # check in that car
    if user_choice == '1':
        return check_in_new_car(particular_parking_db, username)

    # employee in parking decide to checkout exist a car
    elif user_choice == '2':
        return check_out_existed_car(particular_parking_db, username)

    else:
        print('Your Should Enter (1/2)!!!')
        return parking_menu(username)


def log_in_menu():
    """
    a method to authentication existed parking
    :return: if valid authentication transfer users to their profile
             if not transfer them to main menu.
    """
    # get username for login
    username = input('Please Enter Your Username: ').strip()

    # get password for above username to login
    password = input('Please Enter Your Password: ')

    # check this user in our system to exist or not
    user_exist = is_this_user_exist(username, password)

    if user_exist:
        # transfer existed user to its parking menu
        return parking_menu(username)

    # transfer to main menu if user
    return main_menu()


def register_parking_information():
    """
    a method for giving parking info such as:
        parking name,
        parking address,
        parking capacity and
        parking price per minutes.
    :return: if register totally complete done return parking_data_as_bson_format,
             if not return to this menu again.
    """

    # try to get parking information from user
    try:
        print('*' * 60)
        parking_name = input('* Please Enter Your Parking Name: ').strip()
        parking_address = input('* Please Enter Your Parking Address: ').strip()
        parking_capacity = int(input('* Please Enter Your Parking Capacity: '))
        parking_price = int(input('* Please Enter Your Parking Price/Min: '))
        print('*' * 60)

    # if some error occur
    except ValueError:
        print('!' * 60)
        print('! You should a integer number for parking capacity and parking price/min')
        print('!' * 60)

        # return user to register a gain.
        return register_parking_information()

    # user's data enter.
    register_parking_data = f'Parking Name: {parking_name} \n' \
                            f'Parking Address: {parking_address} \n' \
                            f'Parking Capacity: {parking_capacity} \n' \
                            f'Parking Price: {parking_price} \n'

    # assurance about parking information
    if are_you_confirm_these_data(register_parking_data, 'Parking info'):
        # user sure about do these works.
        # create this Parking object
        temp_parking = Park(parking_name,
                            parking_address,
                            parking_capacity,
                            parking_price)

        # convert an object to the json.
        parking_data_as_json_format = json.dumps(temp_parking.__dict__)

        # convert above json to the bson for sending data to mongodb
        parking_data_as_bson_format = loads(parking_data_as_json_format)

        return parking_data_as_bson_format

    # if user doesn't sure do this.
    return register_parking_information()


def sing_up_menu():
    """
    a method for register new parking in our system and allocated its profile.
    :return: if this process completely done without any problems create new parking
             if not and some problems occur in this process user should sign up again.
    """
    # get a user name for this new parking.
    username = input('Please Enter Your Username: ').strip()

    # get a password for this new parking.
    password = input('Please Enter Your Password: ')

    # get password confirmed for confirm their password.
    confirm_password = input('Please Confirm Your Password: ')

    # get new users info and check it with our database.
    is_new_user_created = sign_up_users(username, password, confirm_password)

    # check we can add this user into our system or not
    if is_new_user_created:
        # get parking data as bson form
        bson_data = register_parking_information()

        # create a special database for each parking that new register.
        create_particular_database_for_each_parking(username, bson_data)

        print('@' * 60)
        print('@\t*** Congratulation ***')
        print('@ You created your parking profile')
        print('@ Now you should login')
        print('@' * 60)

        # back user to main to login our system.
        return main_menu()

    return sing_up_menu()


def main_menu():
    """
    This CLI shows main menu to the users.
    :return:
    """
    # context of main menu.
    main_menu_body = f'{"*" * 60} \n' \
                     f'* \t 1.Log In \n' \
                     f'* \t 2.Sing Up \n' \
                     f'{"*" * 60}'

    # show the context of main menu as CLI.
    print(main_menu_body)

    # get user choice.
    user_choice = input('Please Choose Your Choice: ').strip()

    # find out user choice and his/her goal.
    if user_choice == '1':
        # user decide to login into our system.
        return log_in_menu()

    elif user_choice == '2':
        # user decide to sign up into our system.
        return sing_up_menu()

    else:
        # user enter invalid choice
        print('Your Should Enter (1/2)!!!')
        return main_menu()
