import json
from models import Car, Factor, Park
from mongodb_connection import sing_up_check_users, create_database_user, \
    log_in_check_exist_username, client
from bson.json_util import loads, dumps
from datetime import datetime

decorate = '*' * 60


def confirm_car_plaque(car_plaque):
    confirm_plaque = input(f'Car Plaque is: {car_plaque}'
                           f'\n Are You Sure(Y/N) ? ').strip()
    if confirm_plaque in ('Y', 'y'):
        return True
    else:
        create_factor()


def create_factor(data, username):
    db = client[f'{username}']
    collection = db[f'{username}_DATA']
    parking = Park(data['parking_name'], data['parking_address'],
                   data['parking_capacity'], data['price_per_minute'])
    parking.park_place = data['park_place']
    if not parking.is_full():
        car_plaque = input('Please Enter Your Car Plaque: ').strip()

        if confirm_car_plaque(car_plaque):
            # return car_plaque
            car = Car(car_plaque)
            factor = Factor(parking, car)
            factor_collection = db[f'{username}_FACTOR']
            factor_collection.insert_one(loads(json.dumps(factor.__dict__())))
            print(parking.park_place)
            collection.update_one({}, {'$set': {'park_place': parking.park_place}})
            return is_valid_authentication(username, data)
    else:
        print('Parking is full')
        return is_valid_authentication(username, data)


def check_out(username):
    db = client[f'{username}']
    parking_collection = db[f'{username}_DATA']
    data = parking_collection.find_one()
    parking = Park(data['parking_name'], data['parking_address'],
                   data['parking_capacity'], data['price_per_minute'])
    parking.park_place = data['park_place']
    car_plaque = input('Please Enter Car Plaque To Check Out: ').strip()
    if confirm_car_plaque(car_plaque):
        car = Car(car_plaque)
        db = client[f'{username}']
        collection = db[f'{username}_FACTOR']
        data = collection.find_one({'$and': [{'car_plaque': car_plaque}, {'is_out': False}]})
        if data:
            factor = Factor(parking, car)
            date_time_obj = datetime.strptime(data['datetime_in'], '%Y-%m-%d %H:%M:%S.%f')
            factor.datetime_in = date_time_obj
            factor.car_plaque = data['car_plaque']
            factor.total_time_exist_in_parking = data['total_time_exist_in_parking']
            factor.position_park = data['position_park']
            factor.check_out()
            print(factor)
            parking_collection.update_one({}, {'$set': {'park_place': parking.park_place}})
            collection.update_one({'$and': [{'car_plaque': car_plaque}, {'is_out': False}]}, {'$set': {'is_out': True}})

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
    data = log_in_check_exist_username(username, password)
    if data is not False:
        return is_valid_authentication(username, data)
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
        json_parking_data = json.dumps(temp_parking.__dict__)
        serialize_parking_data = loads(json_parking_data)
        return serialize_parking_data
    else:
        return create_parking()


def sing_up():
    username = input('Please Enter Your Username: ').strip()
    password = input('Please Enter Your Password: ')
    confirm_password = input('Please Confirm Your Password: ')
    check = sing_up_check_users(username, password, confirm_password)
    if check:
        data = create_parking()
        create_database_user(username, data)
        print('You Can Now Login.')
        return main_menu()
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
