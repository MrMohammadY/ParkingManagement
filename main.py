from models import Car, Park, Factor
from datetime import datetime


if __name__ == '__main__':
    p1 = Park('atlas', 'iran', 10, 100)
    if not(p1.is_full()):
        c1 = Car('12 h 555 ir 55')
        f1 = Factor(p1, c1)

        f1.datetime_in = datetime(2020, 11, 1)
        f1.check_out()

        print(p1)
        print(f1)

