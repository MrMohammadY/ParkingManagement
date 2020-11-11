import json
from bson.json_util import loads


class Park:
    # for create number of parking and create unit code

    def __init__(self, name, address, capacity, price):
        """
        Set attribute for parking
        :param name: parking name
        :param address: parking address
        :param capacity: parking opacity
        :param capacity: parking price per minute
        """
        # set parking name
        self.parking_name = name

        # set price per minute for parking
        self.price_per_minute = price

        # set parking address
        self.parking_address = address

        # set parking capacity like : 250
        self.parking_capacity = capacity

        # set dictionary for any space of parking capacity like: {1:[True],...}
        self.park_place = dict()
        # append to dict space of parking capacity and
        for i in range(1, self.parking_capacity + 1):
            self.park_place[i] = [True]

        self.serialize = None
        # parking counter for counting parking

    def serialize_information(self):
        data = {
            'ParkingName': self.parking_name,
            'ParkingAddress': self.parking_address,
            'ParkingCapacity': self.parking_capacity,
            'ParkPlace': self.park_place,
            'ParkingPrice': self.price_per_minute
        }
        json_data = json.dumps(data)
        serialize = loads(json_data)
        self.serialize = serialize

    def __str__(self):
        # decorate is a * frame for top and bottom parking info.
        decorate = '*' * 60

        # text of body parking info
        print_parking_info = f'{decorate}\n' \
                             f'*\t Parking Name: {self.parking_name}\n' \
                             f'*\t Parking Capacity: {self.parking_capacity}\n' \
                             f'*\t Parking Address: {self.parking_address}\n' \
                             f'*\t Parking Price: {self.price_per_minute}\n' \
                             f'{decorate}'

        return print_parking_info

    def is_full(self):
        """
        Checking that the parking lot is full?
        :return: True: parking is full || False: parking is free
        """
        return all(status[0] is False for status in self.park_place.values())

    def report_free_park_place(self):
        """
        check self.parking_place and if place is True(free) append to list
        :return: list of free park place
        """
        list_of_free_park_place = list()

        for key, val in self.park_place.items():
            if val[0]:
                list_of_free_park_place.append(key)

        return list_of_free_park_place

    def report_busy_park_place(self):
        """
        check self.parking_place and if place is False(busy) append to list
        :return: list of busy park place
        """
        list_of_busy_park_place = list()

        for key, val in self.park_place.items():
            if val[0] is False:
                list_of_busy_park_place.append(key)

        return list_of_busy_park_place

    def update_list_of_free_park_place(self, position_park, plaque, is_out):
        for k, v in self.park_place.items():
            if is_out is False:
                if position_park == k:
                    self.park_place[k] = [False, plaque]
            elif is_out:
                if position_park == k:
                    self.park_place[k] = [True]

    def show_information_about_busy_park_place(self, list_of_busy_park_place,
                                               number_busy_park_place):
        """
        take number of place for check car plaque
        :param list_of_busy_park_place: take list of busy place
        :param number_busy_park_place: take number of place for check
        :return:
        """
        if len(list_of_busy_park_place) == 0:
            print('All place is free!')

        elif number_busy_park_place in list_of_busy_park_place:
            info = self.park_place[number_busy_park_place]
            print(f'this plaque: {info[1]}\n for'
                  f'this place {number_busy_park_place}')

        else:
            print('This position is free!')

    def find_free_park_place(self, list_of_free_park_place):
        """
        take list of free place and return first free place to Factor
        :param list_of_free_park_place: take list of free place
        :return: number of free place
        """
        return list_of_free_park_place[0]

    def update_price_per_minute(self, price):
        """
        take new price and update price_per_minute
        :param price: new price
        """
        self.price_per_minute = price

