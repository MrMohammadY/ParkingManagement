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
