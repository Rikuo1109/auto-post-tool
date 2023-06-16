from ninja.schema import Schema

class UserRegisterRequest(Schema):
    first_name: str
    last_name: str
    email: str
    username: str
    password: str


class UserLoginRequest(Schema):
    username: str
    password: str