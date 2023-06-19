from ninja.schema import Schema
from ninja.orm import create_schema
from ..models import Post, PostManagement

PostSchema = create_schema(Post)
PostManagementSchema = create_schema(PostManagement)


class PostRequest(Schema):
    post: PostSchema
    post_management: PostManagementSchema
