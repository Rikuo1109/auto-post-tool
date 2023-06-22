from ninja import Schema, ModelSchema
from ninja.orm import create_schema
from ..models import Post, PostManagement
from .response import PostResponse


class PostRequest(Schema):
    post: PostResponse
    # post_management: PostManagementSchema
