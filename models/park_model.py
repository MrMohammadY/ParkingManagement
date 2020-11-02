class Park:
    parking_counter = 0  # for create number of parking and create unit code

    def __init__(self, name, address, capacity):
        """
        Set attribute for parking
        :param name: parking name
        :param address: parking address
        :param capacity: parking opacity
        """
        self.parking_id = Park.parking_counter + 1  # create a unit code for parkings
        self.parking_name = name
        self.parking_address = address
        self.parking_capacity = capacity
        self.park_place = dict()

        for i in range(1, self.parking_capacity + 1):
            self.park_place[i] = [True]

        Park.parking_counter += 1

    def is_full(self):
        """
        Checking that the parking lot is full?
        :return: True: parking is full || False: parking is free
        """
        return all(status[0] is False for status in self.park_place.values())

    def report_free_park_place(self):
        """
        :return: list of free park place
        """
        list_of_free_park_place = list()

        for key, val in self.park_place.items():
            if val[0]:
                list_of_free_park_place.append(key)

        return list_of_free_park_place

    def report_busy_park_place(self):
        """
        :return: list of busy park place
        """
        list_of_busy_park_place = list()

        for key, val in self.park_place.items():
            if val[0] is False:
                list_of_busy_park_place.append(key)

        return list_of_busy_park_place

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
