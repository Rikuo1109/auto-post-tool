from ninja.schema import Schema


class LoginSchema(Schema):
    username: str
    password: str
