from ninja.schema import  Schema

class LoginSchema(Schema):
    email: str
    password: str