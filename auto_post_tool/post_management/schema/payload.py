from ninja.schema import Schema


class PostSchema(Schema):
    content: str
    post_type: str
