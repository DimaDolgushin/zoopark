from typing import Callable, Any
import settings
import requests
from src.server.base.models import User, Zoo


def server_available(func) -> Callable[[tuple[Any, ...], dict[str, Any]], dict[str, str] | Any]:
    def need_it(*args, **kwargs):
        try:
            answer = requests.get(url=settings.URL)
            return func(answer, *args, **kwargs)
        except requests.exceptions.ConnectionError:
            return {"code": 400, "message": f'Server not available', "result": None}

    return need_it


#  User
@server_available
def check_login(answer_connect: None = None, login: str = '', password: str = '') -> dict:
    answer = requests.get(
        url=f'{settings.URL}/users/login',
        data=f'{{ "login": "{login}", "password": "{password}" }}').json()
    return answer


@server_available
def register(answer_connect: None = None, user: User = User) -> dict:
    answer = requests.post(
        url=f'{settings.URL}/users/new',
        data=f'{{ "login": "{user.login}", "password": "{user.password}", "power_level": "{user.power_level}" }}').json()
    return answer


@server_available
def update(answer_connect: None = None, user: User = User):
    answer = requests.put(
        url=f'{settings.URL}/users/update/{user.id}',
        data=f'{{ "login": "{user.login}", "password": "{user.password}" }}'
    ).json()
    return answer


# Zoo
@server_available
def create_zoo(answer_connect: None = None, zoo: Zoo = Zoo):
    answer = requests.post(
        url=f'{settings.URL}/zoos/new',
        data=f' {{ "title": "{zoo.title}", "city": "{zoo.city_id}", "phone": "{zoo.phone}" }}'
    ).json()
    return answer


@server_available
def update_zoo(answer_connect: None = None, zoo: Zoo = Zoo):
    data = f'{{ "title": "{zoo.title}", "city_id": "{zoo.city_id}, "phone": "{zoo.phone}" }}'
    answer = requests.put(
        url=f'{settings.URL}/zoos/update/{zoo.id}',
        data=data
    ).json()
    return answer


def get_all_zoos(answer_connect: None = None):
    return requests.get(
        url=f'{settings.URL}/zoos/get_all'
    ).json()


def get_city_by_id(answer_connect: None = None, id: int = 0):
    return requests.get(
        url=f'{settings.URL}/cities/get/{id}').json()


def get_all_cities(answer_connect: None = None):
    return requests.get(
        url=f'{settings.URL}/cities/get_all'
    ).json()


def get_ticket_by_id(answer_connect: None = None):
    pass  # TODO
