from django.db import transaction

from .apis.facebook import GroupsApiFacebookService, PagesApiFacebookService
from .post import CreatePostService, GetDetailPostService, RemovePostService, UpdatePostDetailService
from .post_management import CreatePostManagementService, RemovePostManagementService, UpdatePostManagementService
from image_management.models import ImagePost
from post_management.models.post import Post, PostManagement
from utils.enums.post import FacebookPlatFormEnum, PostManagementPlatFormEnum
from utils.functions.filters import FiltersUtils


class Service:
    def __init__(self, request):
        self.request = request

    @transaction.atomic
    def create_post_service(self, data):
        service = CreatePostService(user=self.request.user, content=data.content, post_type=data.post_type)
        post = service()
        service = CreatePostManagementService(post=post, managements=data.managements)
        post_managements = service()
        return post

    def update_post_details_service(self, uid, data):
        post = Post.get_by_uid(uid=uid)
        service = UpdatePostDetailService(post=post, data=data)
        return service()

    def get_matrix_post_service(self, filters, sorting, sort_type):
        sort_field = FiltersUtils.get_format_sort_type(sorting=sorting, sort_type=sort_type)
        posts = Post.objects.filter(filters.get_filter_expression(), user__exact=self.request.user).order_by(sort_field)
        for post in posts:
            post.images = ImagePost.filter_by_post(post=post)
        return posts

    def get_matrix_post_management_service(self, filters, sorting, sort_type):
        sort_field = FiltersUtils.get_format_sort_type(sorting=sorting, sort_type=sort_type)
        posts = Post.filter_by_user(user=self.request.user)
        return PostManagement.objects.filter(filters.get_filter_expression(), post__in=posts).order_by(sort_field)

    def get_detail_post_service(self, uid):
        service = GetDetailPostService(uid)
        post = service()
        post.managements = PostManagement.filter_by_post(post=post)[:10]
        return post

    def view_post_management_from_post_service(self, uid):
        return PostManagement.filter_by_post(post=Post.get_by_uid(uid=uid))

    def remove_post_service(self, uid):
        service = RemovePostService(uid)
        service()

    def create_post_management_service(self, uid, data):
        post = Post.get_by_uid(uid=uid)
        service = CreatePostManagementService(post=post, managements=data.managements)
        service()

    def update_post_management_service(self, uid, data):
        post_management = PostManagement.get_by_uid(uid=uid)
        service = UpdatePostManagementService(post_management=post_management, management=data)
        service()

    def remove_post_management_service(self, uid):
        post_management = PostManagement.get_by_uid(uid=uid)
        service = RemovePostManagementService(post_management=post_management)
        return service()

    def publish_post_management_service(self, uid):
        """
        Publish post base on platform: FACEBOOK, ZALO
        FACEBOOK:
        * Personal to group
        * Page to group
        * Page to page
        scheduled_publish_time (unix_timestamp, from 10 minutes to 75 days) just available in pages
        formatting just available in groups
        """
        post_management = PostManagement.get_by_uid(uid=uid)
        post = post_management.post
        user_id = "100013449046092"
        if post_management.platform == PostManagementPlatFormEnum.FACEBOOK:
            """TODO"""
            select = FacebookPlatFormEnum.PAGE
            """"""
            if select == FacebookPlatFormEnum.PAGE:
                page_id = "111255372005139"
                access_token = "EAAECSZAzYmwwBAGlXTMYyE4hoZBgaqBpRQZAvpZBO1OvHtmawVOpq2fqwuVNfldY98jBg4c1tg7TZALnMJs3L7l0KhVU1mkaXV5a3ZBQVinD6JOJDkY2ZAyZBX0fZA8bO2ueoTqBBBMTtPD5MOXnZA2po2YcAZAk9w5LooPz45VA5lEUFVC4j4DqVDS5GC0fAzTGYLx7lnTu49OK6FSPAdjgLZAw4UqhCszLRy4ZD"
                message = post.content
                service = PagesApiFacebookService(access_token=access_token, page_id=page_id)
                response = service.publish_feed(
                    message=message, scheduled_publish_time_unix_timestamp=post_management.time_posting.timestamp()
                )
            elif select == FacebookPlatFormEnum.GROUP:
                group_id = "1034782201238472"
                message = """**Goodnight!**"""
                access_token = "EAAECSZAzYmwwBAJAYQjfvZC3CvBZBV1v6snTWgCRg9DsSLptSogIZAZArir1QWPWqXDn6ZBgcayIdJWYjrFHfq72PjoAo837vz7Ffd4BJ5M3Fi728RXgdEnll3dYr119WX7CZB1MBMkzCKq7XNzFcCth8I2Cvfn14GmEUAY96iFFHZCgvZBmxZCnBH3uTgwd1ws61qyPwmE5K3crHpzZANPgz49b3av7ylz8iiTYPpbWw4ZAI4uZCuHroVnUZBtLF4qlJn3LEZD"
                service = GroupsApiFacebookService(access_token=access_token, group_id=group_id)
                response = service.publish_feed(message=message)
