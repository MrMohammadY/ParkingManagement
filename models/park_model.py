class Park:
    parking_counter = 0

    def __init__(self, name, address, capacity):
        self.parking_id = Park.parking_counter + 1
        self.parking_name = name
        self.parking_address = address
        self.parking_capacity = capacity
        self.park_place = dict()

        for i in range(1, self.parking_capacity + 1):
            self.park_place[i] = [True]

        Park.parking_counter += 1

    def is_full(self):
        return all(status[0] is False for status in self.park_place.values())

    def report_free_park_place(self):
        list_of_free_park_place = list()

        for key, val in self.park_place.items():
            if val[0]:
                list_of_free_park_place.append(key)

        return list_of_free_park_place

    def report_busy_park_place(self):
        list_of_busy_park_place = list()

        for key, val in self.park_place.items():
            if val[0] is False:
                list_of_busy_park_place.append(key)

        return list_of_busy_park_place

    def show_information_about_busy_park_place(self, list_of_busy_park_place,
                                               number_busy_park_place):
        if len(list_of_busy_park_place) == 0:
            print('All place is free!')

        elif number_busy_park_place in list_of_busy_park_place:
            info = self.park_place[number_busy_park_place]
            print(f'this plaque: {info[1]}\n for'
                  f'this place {number_busy_park_place}')
        else:
            print('This position is free!')

    def find_free_park_place(self, list_of_free_park_place):
        return list_of_free_park_place[0]

