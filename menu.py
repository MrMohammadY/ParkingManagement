import json
from models import Car, Factor, Park, SingUp, LogIn
from config import client
from bson.json_util import loads
from datetime import datetime

decorate = '*' * 60


def create_factor(data, username):
    db = client[f'{username}']
    collection = db[f'{username}_DATA']
    parking = Park(data['ParkingName'], data['ParkingAddress'],
                   data['ParkingCapacity'], data['ParkingPrice'])
    parking.park_place = data['ParkPlace']

    if not parking.is_full():
        car_plaque = input('Please Enter Your Car Plaque: ').strip()
        car = Car(car_plaque)
        if car.confirm_car_plaque():
            factor = Factor(parking, car)
            factor.serialize_information()
            factor_collection = db[f'{username}_FACTOR']
            factor_collection.insert_one(factor.serialize)
            print(parking.park_place)
            collection.update_one({},
                                  {'$set': {'ParkPlace': parking.park_place}})
            return is_valid_authentication(username, data)
        else:
            create_factor(data, username)
    else:
        print('Parking is full')
        return is_valid_authentication(username, data)


def check_out(username):
    db = client[f'{username}']
    parking_collection = db[f'{username}_DATA']
    data = parking_collection.find_one()
    parking = Park(data['ParkingName'], data['ParkingAddress'],
                   data['ParkingCapacity'], data['ParkingPrice'])
    parking.park_place = data['ParkPlace']
    car_plaque = input('Please Enter Car Plaque To Check Out: ').strip()
    car = Car(car_plaque)
    if car.confirm_car_plaque():
        db = client[f'{username}']
        collection = db[f'{username}_FACTOR']
        data = collection.find_one(
            {'$and': [{'car_plaque': car_plaque}, {'is_out': False}]})
        if data:
            factor = Factor(parking, car)
            date_time_obj = datetime.strptime(data['datetime_in'],
                                              '%Y-%m-%d %H:%M:%S.%f')
            factor.datetime_in = date_time_obj
            factor.car_plaque = data['car_plaque']
            factor.total_time_exist_in_parking = data[
                'total_time_exist_in_parking']
            factor.position_park = data['position_park']
            factor.check_out()
            print(factor)
            parking_collection.update_one({}, {
                '$set': {'ParkPlace': parking.park_place}})
            collection.update_one(
                {'$and': [{'car_plaque': car_plaque}, {'is_out': False}]},
                {'$set': {'is_out': True}})
            return is_valid_authentication(username)

        else:
            print('This Plaque is nit exist!')
            return check_out(username)


def is_valid_authentication(username, data):
    print(f'{decorate}\n'
          f'{username} Welcome To Your Panel \n'
          f'1. New Factor \n'
          f'2. Check out \n'
          f'{decorate}')

    user_choice = input('Please Choose Your Choice: ').strip()
    if user_choice == '1':
        return create_factor(data, username)
    elif user_choice == '2':
        return check_out(username)
    else:
        print('Your Should Enter (1/2)!!!')
        return is_valid_authentication(username, data)


def log_in():
    username = input('Please Enter Your Username: ').strip()
    password = input('Please Enter Your Password: ')
    login = LogIn(username, password)

    if login.check_username():
        return is_valid_authentication(login.UserName, login.return_data())
    else:
        return main_menu()


def create_parking():
    try:
        parking_name = input('Please Enter Your Parking Name: ').strip()
        parking_address = input('Please Enter Your Parking Address: ').strip()
        parking_capacity = int(input('Please Enter Your Parking Capacity: '))
        parking_price = int(input('Please Enter Your Parking Price: '))
    except ValueError:
        print('Type Of Parking Capacity And Parking price should be integer')
        return create_parking()

    print(f'You Enter This Information: \n'
          f'Parking Name: {parking_name} \n'
          f'Parking Address: {parking_address} \n'
          f'Parking Capacity: {parking_capacity} \n'
          f'Parking Price: {parking_price} \n')

    confirm_parking_info = input('Are You Sure About This Information(Y/N): ')

    if confirm_parking_info in ('Y', 'y'):
        temp_parking = Park(
            parking_name, parking_address, parking_capacity, parking_price
        )
        temp_parking.serialize_information()
        return temp_parking.serialize
    else:
        return create_parking()


def sing_up():
    first_name = input('Please Enter Your Name: ')
    family_name = input('Please Enter Family: ')
    username = input('Please Enter Your Username: ').strip()
    password = input('Please Enter Your Password: ')
    confirm_password = input('Please Confirm Your Password: ')
    email = input('Please Enter Email: ')
    phone = input('Please Enter Phone: ')

    new_user = SingUp(
        first_name, family_name, username, password, confirm_password, email,
        phone
    )
    if new_user.create_user():
        data = create_parking()

        try:
            new_user.insert_user_to_mongodb_users()
            new_user.create_user_database(data)
        except BaseException:
            print('Some Problems Occurred In Your Sing Up Process,'
                  ' Please Try Later!')
            new_user.delete_user()
            return sing_up()
        return sing_up()

    else:
        return sing_up()


def main_menu():
    main_menu_body = f'{decorate} \n' \
                     f'* \t 1.Log In \n' \
                     f'* \t 2.Sing Up \n' \
                     f'{decorate}'
    print(main_menu_body)

    user_choice = input('Please Choose Your Choice: ').strip()

    if user_choice == '1':
        return log_in()

    elif user_choice == '2':
        return sing_up()
    else:
        print('Your Should Enter (1/2)!!!')
        return main_menu()


main_menu()
