from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import ProfileUser
from json import loads, JSONDecodeError
import re
from django.http.request import QueryDict
from string import ascii_lowercase, ascii_uppercase, digits


def validate_all_new_user_data(data: dict):
    if User.objects.filter(username=data.get('username', '')).exists():
        raise ValidationError('Пользователь с таким username уже существует.')

    validate_fullname_user(fullname=data.get('name', ''))
    validate_password_user(password=data.get('password', ''))


def get_update_user_data(data: dict, user: ProfileUser) -> tuple:
    return data.get('fullName', user.fullName), data.get('phone', user.phone), data.get('email', user.email)


def validate_fullname_user(fullname: str):
    if len(fullname.split()) != 3:
        raise ValidationError(PERSONAL_DATA_ERROR)

    if any(letter.isdigit() for letter in fullname):
        raise ValidationError('В полном имени не должно быть цифр.')


def validate_phone_user(old_phone: str, new_phone: str):
    if re.fullmatch(r'Неизвестно|^[78]\d{10}$|^\+7\d{10}$', new_phone) is None:
        raise ValidationError('Некорректный номер телефона')

    if new_phone != 'Неизвестно' and old_phone != new_phone and ProfileUser.objects.filter(phone=new_phone).exists():
        raise ValidationError('Пользователь с таким номером телефона уже существует.')


def check_email_user_exists(old_email: str, new_email: str):
    if old_email != new_email and ProfileUser.objects.filter(email=new_email).exists():
        raise ValidationError('Пользователь с таким email уже существует.')


def check_username_exists(username: str):
    if User.objects.filter(username=username).exists():
        raise ValidationError('Пользователь с таким username уже существует.')


def validate_password_user(password: str):
    SPECIAL_SYMBOLS = '!@#$%^&*()—_+=;:,./?\|`~[]{}'

    if not all([any((sym in ascii_lowercase) for sym in password),
                any((sym in ascii_uppercase) for sym in password),
                any((sym in digits) for sym in password),
                any((sym in SPECIAL_SYMBOLS) for sym in password),
                len(password) > 7]):
        raise ValidationError(WEAK_PASSWORD_ERROR)


def validate_file(namefile: str, size: int):
    if not namefile.endswith(('.jpg', '.png', '.jpeg', '.gif')):
        raise ValidationError('Файл должен быть изображением')

    if not size < 2_097_152:
        raise ValidationError('Размер файла не должен превышать 2МБ')


def get_classic_dict(dict_string: QueryDict[str] | dict) -> dict:
    for nice_dict in dict_string:
        try:
            username_and_psw_dict = loads(nice_dict)
            return username_and_psw_dict
        except JSONDecodeError:
            return dict_string


def get_data_new_user(data_user: dict) -> tuple:
    name, surname, patronymic = data_user.get('first_name', 'Н. Н. Н.').split()
    return name, surname, patronymic, data_user.get('username', ''), data_user.get('password', '')


def create_new_user(name: str, surname: str, login_user: str, psw_user: str) -> User:
    new_user: User = User.objects.create_user(username=login_user,
                                              password=psw_user)
    new_user.first_name, new_user.last_name = name, surname
    new_user.save()
    return new_user


def create_profile_new_user(new_user: User, name: str, surname: str, patronymic: str):
    profile_new_user: ProfileUser = ProfileUser.objects.create(user=new_user)
    profile_new_user.fullName = f'{name} {surname} {patronymic}'
    profile_new_user.save()


WEAK_PASSWORD_ERROR = 'Пароль должен состоять минимум из 8 символов.\n' \
                      'В нем должны быть буквы в верхнем и нижнем регистрах латинского алфавита, цифры и спецсимволы\n' \
                      '!@#$%^&*()—_+=;:,./?\|`~[]{}'

PERSONAL_DATA_ERROR = 'Нужно ввести имя, фамилию и отчество через пробел'




