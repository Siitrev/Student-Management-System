import re


class NameValidaionException(Exception):
    "Exception thrown when name variable is invalid"

    def __init__(self):
        message = "Name is invalid"
        super().__init__(message)


class PhoneValidaionException(Exception):
    "Exception thrown when phone number variable is invalid"

    def __init__(self):
        message = "Phone number is invalid"
        super().__init__(message)


def name_validation(name):
    pattern = re.compile(r"^[a-zA-Z ]{2,}$")
    if not re.match(pattern,name):
        raise NameValidaionException

def phone_validation(number):
    pattern = re.compile(r"^((\(\+{1}\d{2}\){1}\d{9})|(\d{9}))$")
    if not re.match(pattern,number):
        raise PhoneValidaionException
