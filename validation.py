from datetime import datetime


class Validator:

    def __init__(self):
        pass

    @staticmethod
    def phone(number):
        if number.isdigit() and len(number) == 10:
            return number
        return None

    @staticmethod
    def date(datetime_str):
        now = datetime.now()
        if datetime_str == 'now':
            return now
        try:
            datetime_object = datetime.strptime(datetime_str, '%y-%m-%d %H:%M')
            return datetime_object
        except ValueError:
            return None

