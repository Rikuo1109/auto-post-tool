from django.db import transaction

from .apis.services import ApiGetInteractionsService, ApiPublishService
from .post import CreatePostService, GetDetailPostService, RemovePostService, UpdatePostDetailService
from .post_management import CreatePostManagementService, RemovePostManagementService
from image_management.models import ImagePost
from post_management.models.post import Post, PostManagement
from post_management.schema.payload import PostRequest
from utils.enums.post import PostManagementStatusEnum
from utils.functions.filters import FiltersUtils
from utils.functions.validator import ValidatorsUtils


class Service:
    def __init__(self, request):
        self.request = request

    @transaction.atomic
    def create_post_service(self, data: PostRequest):
        """json dumps will turn the list of post_type into string literal"""
        service = CreatePostService(user=self.request.user, content=data.content, post_type=data.post_type)
        post = service()

        if len(data.images) > 0:
            post.images.add(*ImagePost.filter_by_uids(uids=data.images))

    def update_post_details_service(self, uid, data):
        post = Post.get_by_uid(uid=uid)
        ValidatorsUtils.validator_user_post(user=self.request.user, post=post)
        service = UpdatePostDetailService(post=post, data=data)
        return service()

    def get_matrix_post_service(self, filters, sorting, sort_type):
        sort_field = FiltersUtils.get_format_sort_type(sorting=sorting, sort_type=sort_type)
        return Post.objects.filter(
            FiltersUtils.filters_translate(filters=filters, handle_function=FiltersUtils.handle_post_filter_dict),
            user__exact=self.request.user,
        ).order_by(sort_field)

    def get_detail_post_service(self, uid):
        service = GetDetailPostService(uid)
        post = service()
        post.set_type_list()
        ValidatorsUtils.validator_user_post(user=self.request.user, post=post)
        return post

    def view_post_management_detail_service(self, uid):
        post_management = PostManagement.get_by_uid(uid=uid)
        ValidatorsUtils.validator_user_post_management(user=self.request.user, post_management=post_management)
        service = ApiGetInteractionsService(post_management)
        post_management.reactions = service.get_all_reactions()
        post_management.comments = service.get_all_comments()
        post_management.content = post_management.post.content
        post_management.images = post_management.post.images
        return post_management

    def view_post_management_of_post_service(self, uid, filters, sorting, sort_type):
        post = Post.get_by_uid(uid=uid)
        ValidatorsUtils.validator_user_post(user=self.request.user, post=post)
        sort_field = FiltersUtils.get_format_sort_type(sorting=sorting, sort_type=sort_type)
        return PostManagement.objects.filter(
            FiltersUtils.filters_translate(
                filters=filters, handle_function=FiltersUtils.handle_post_management_of_post_filter_dict
            ),
            post=post,
        ).order_by(sort_field)

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
        response_list = []
        for post_management in post_managements:
            service = ApiPublishService(post_management)
            response_service = service()

            response_item = {
                "uid": post_management.uid,
                "message": response_service,
                "status": PostManagementStatusEnum.SUCCESS,
            }
            if "error" in response_service:
                response_item["status"] = PostManagementStatusEnum.FAIL

            response_list.append(response_item)
        return response_list
