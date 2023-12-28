from typing import Optional
from pydantic import BaseModel


class BaseModelModify(BaseModel):
    id: Optional[int]


class Person(BaseModelModify):
    surname: str
    post_id: int
    name: str
    patronymic: str
    date_birth: str


class Zoo(BaseModelModify):
    title: str
    phone: str
    city_id: int


class UserLogin(BaseModelModify):
    login: str
    password: str


class City(BaseModelModify):
    title: str


class User(UserLogin):
    power_level: int = 1


class Ticket(BaseModelModify):
    zoo_id: int
    user_id: int
    date: str
