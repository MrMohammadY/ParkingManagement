from datetime import datetime


class Factor:
    def __init__(self, park, car):
        """
        :param park: composition with Park class
        :param car: composition with Car class
        """

        self.park = park
        self.car = car

        # position_park: car position in parking.
        self.position_park = self.park.find_free_park_place(
            self.park.report_free_park_place())

        # datetime_in: register car check in date time.
        self.datetime_in = datetime.now()

        # datetime_out: register car check out date time.
        self.datetime_out = None

        # total time a car exist in a specific parking.
        self.total_time_exist_in_parking = 0

        # car_plaque: register plaque of car
        self.car_plaque = self.car.plaque

        # price_of_factor: total price when check out.
        self.price_of_factor = 0

        # is_out: if car exit or not.
        self.is_out = False

        # update list of free park place based on cars check in.
        self.park.update_list_of_free_park_place(self.position_park,
                                                 self.car_plaque, self.is_out)

    def __dict__(self):
        return {
            'position_park': self.position_park,
            'datetime_in': str(self.datetime_in),
            'datetime_out': self.datetime_out,
            'total_time_exist_in_parking': self.total_time_exist_in_parking,
            'car_plaque': self.car_plaque,
            'price_of_factor': self.price_of_factor,
            'is_out': self.is_out
        }

    def __str__(self):
        # decorate is a * frame for top and bottom receipt.
        decorate = '*' * 60

        # text of body receipt or text main of factor
        print_factor = f'{decorate}\n' \
                       f'*\t Car plaque is: {self.car_plaque}\n' \
                       f'*\t Car park place is: {self.position_park}\n' \
                       f'*\t Check in Date Time: {self.datetime_in}\n' \
                       f'*\t Check out Date Time: {self.datetime_out}\n' \
                       f'*\t Number of minutes you exist in parking: {self.total_time_exist_in_parking}\n' \
                       f'*\t Price per Minutes in this parking: {self.park.price_per_minute}\n' \
                       f'*\t Total price is: {self.price_of_factor}\n' \
                       f'{decorate}'

        return print_factor

    def __calculate_price_of_factor(self):
        """
        calculate base on total minutes car exist in parking
        :return: total price of factor
        """

        # get price per minute based on current parking
        price_per_min = self.park.price_per_minute

        # calculate difference between date time check out and check in
        pure_min = self.datetime_out - self.datetime_in

        # calculate number of minutes that car exist in parking
        # and update total_time_exist_in_parking object attr
        self.total_time_exist_in_parking = int(pure_min.total_seconds() / 60)

        # calculate total price based on total_time_in_parking and price_per_min
        total_price = price_per_min * self.total_time_exist_in_parking

        return total_price

    def check_out(self):
        """
        some updates happen when car check out the parking
        :return:
        """
        # automate get date time now and update blank value
        self.datetime_out = datetime.now()

        # update situation of car when car leave parking
        self.is_out = True

        # get price of factor and update blank value
        self.price_of_factor = self.__calculate_price_of_factor()

        self.park.update_list_of_free_park_place(self.position_park,
                                                 self.car_plaque, self.is_out)
