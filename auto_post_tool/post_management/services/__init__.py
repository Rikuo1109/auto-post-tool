from django.db import transaction

from .apis.services import ApiGetInteractionsService
from .post import CreatePostService, GetDetailPostService, RemovePostService, UpdatePostDetailService
from .post_management import CreatePostManagementService, RemovePostManagementService
from image_management.models import ImagePost
from post_management.models.post import Post, PostManagement
from post_management.schema.payload import PostRequest
from post_management.services.post_management.publish_post_managements import PublishPostManagements
from post_management.services.utils.filters import PostFiltersUtils
from utils.functions.filters import FiltersUtils
from utils.functions.validator import ValidatorsUtils

import re

import json


class Service:
    def __init__(self, request):
        self.request = request

    @transaction.atomic
    def create_post_service(self, data: PostRequest):
        """json dumps will turn the list of post_type into string literal"""
        service = CreatePostService(user=self.request.user, data=data)
        post = service()

        if len(data.images) > 0:
            post.images.add(*ImagePost.filter_by_uids(uids=data.images))

        return post

    def update_post_details_service(self, uid, data):
        post = Post.get_by_uid(uid=uid)
        ValidatorsUtils.validator_user_post(user=self.request.user, post=post)
        service = UpdatePostDetailService(post=post, data=data)
        return service()

    def get_matrix_post_service(self, filters, filters_custom, sorting, sort_type):
        sort_field = FiltersUtils.get_format_sort_type(sorting=sorting, sort_type=sort_type)
        return Post.objects.filter(
            filters.get_filter_expression(),
            PostFiltersUtils.filters_translate(
                filters=filters_custom, handle_function=PostFiltersUtils.handle_post_filter_dict
            ),
            user__exact=self.request.user,
        ).order_by(sort_field)

    def get_detail_post_service(self, uid):
        service = GetDetailPostService(uid)
        post = service()
        ValidatorsUtils.validator_user_post(user=self.request.user, post=post)
        return post

    def view_post_management_detail_service(self, uid):
        post_management = PostManagement.get_by_uid(uid=uid)
        ValidatorsUtils.validator_user_post_management(user=self.request.user, post_management=post_management)

        service = ApiGetInteractionsService(post_management)
        service()
        post_management.reactions = len(service.get_all_reactions())
        post_management.comments = len(service.get_all_comments())
        post_management.share = len(service.get_all_shares())
        post_management.images = post_management.post.images
        post_management.title = post_management.post.title
        return post_management

    def view_post_management_of_post_service(self, uid, filters, sorting, sort_type):
        post = Post.get_by_uid(uid=uid)
        ValidatorsUtils.validator_user_post(user=self.request.user, post=post)
        sort_field = FiltersUtils.get_format_sort_type(sorting=sorting, sort_type=sort_type)
        return PostManagement.objects.filter(filters.get_filter_expression(), post=post).order_by(sort_field)

    def remove_post_service(self, uid):
        post = Post.get_by_uid(uid=uid)
        ValidatorsUtils.validator_user_post(user=self.request.user, post=post)
        service = RemovePostService(post)
        service()

    def create_post_management_service(self, uid, data):
        post = Post.get_by_uid(uid=uid)
        service = CreatePostManagementService(post=post, managements=data.managements)
        return service()

    def remove_post_management_service(self, uid):
        post_management = PostManagement.get_by_uid(uid=uid)
        ValidatorsUtils.validator_user_post_management(user=self.request.user, post_management=post_management)
        service = RemovePostManagementService(post_management=post_management)
        return service()

    def publish_post_managements_service(self, data):
        service = CreatePostManagementService(post=Post.get_by_uid(data.post_uid), managements=data.managements)
        post_managements = service()
        service = PublishPostManagements(post_managements)
        return service()
