from ninja.schema import Schema


class UserRegisterRequest(Schema):
    first_name: str
    last_name: str
    email: str
    username: str
    password: str


class UserLoginRequest(Schema):
    email: str
    password: str


class UserChangePassword(Schema):
    current_password: str
    new_password: str


class UserUpdateInfoRequest(Schema):
    first_name: str
    last_name: str
    username: str

class UserEmailRequest(Schema):
    email: str


class UserPasswordResetRequest(Schema):
    token: str
    password: str
