from src.client.api import resolvers
from src.server.base.models import User


class Session:
    auth: bool = False
    user: User = User(
        id=0,
        login="",
        password="",
        power_level=0
    )
    error = None
    server_available: bool = False

    def login(self, login, password) -> None:
        answer: dict = resolvers.check_login(login, password)
        user = answer["result"]
        match answer:
            case {"code": 400, "message": message}:
                self.error = message

            case {"code": 200}:
                self.user = User(
                    id=user["id"],
                    login=user["login"],
                    password=user["password"],
                    power_level=user["power_level"]
                )
                self.auth = True

    def register(self, user: User) -> None:
        answer: dict = resolvers.register(user)

        match answer:
            case {"code": 400, "message": message}:
                self.error = message
            
            case {"code": 200}:
                pass

    def update(self, user):
        answer: dict = resolvers.update(user)
        user = answer["result"]
        match answer:
            case {"code": 400, "message": message}:
                self.error = message

            case {"code": 200}:
                self.user = User(
                    id=user["id"],
                    login=user["login"],
                    password=user["password"],
                    power_level=user["power_level"]
                )

    def clear(self):
        self.auth: bool = False
        self.user: User = User(
            id=0,
            login="",
            password="",
            power_level=0
        )

