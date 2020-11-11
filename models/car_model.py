class Car:

    def __init__(self, plaque, model='', company='', color=''):
        """
        set attribute for cars
        :param plaque: take plaque
        :param model: optional | take model car
        :param company: optional | take company car
        :param color: optional | take color car
        """
        self.plaque = plaque
        self.model = model
        self.company = company
        self.color = color

    def confirm_car_plaque(self):
        confirm_plaque = input(f'Car Plaque is: {self.plaque}'
                               f'\n Are You Sure(Y/N) ? ').strip()
        if confirm_plaque in ('Y', 'y'):
            return True
        else:
            return False
