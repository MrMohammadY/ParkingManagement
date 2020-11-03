from datetime import datetime


class Factor:
    def __init__(self, park, car):
        """
        :param park: composition with Park class
        :param car: composition with Car class
        """

        self.park = park
        self.car = car

        # position_park: car position in parking
        self.position_park = self.park.find_free_park_place()

        # datetime_in: register car check in date time.
        self.datetime_in = datetime.now()

        # datetime_out: register car check out date time.
        self.datetime_out = None

        # car_plaque: register plaque of car
        self.car_plaque = self.car.plaque

        # price_of_factor: total price when check out
        self.price_of_factor = 0

        # is_out: if car exit or not
        self.is_out = False

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
        total_time_in_parking = int(pure_min.total_seconds() / 60)

        # calculate total price based on total_time_in_parking and price_per_min
        total_price = price_per_min * total_time_in_parking

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

