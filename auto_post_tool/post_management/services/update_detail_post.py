from django.db import transaction

from post_management.models.post import Post, PostManagement


class UpdatePostDetailService:
    def __init__(self, uid, content=None, post_type=None, managements=None):
        self.uid = uid
        self.content = content
        self.post_type = post_type
        self.managements = managements

    def modify_content(self):
        post = Post.objects.get(uid=self.uid)
        if self.content is not None:
            post.content = self.content
        if self.post_type is not None:
            post.post_type = self.post_type
        return post

    def modify_exist_managements(self):
        managements = PostManagement.objects.filter(uid__in=[_.uid for _ in self.managements])
        for index, management in enumerate(managements):
            if management.status == "pending" and management.auto_publish == True:
                """post is being in queue"""
            elif management.status == "pending" and management.auto_publish == False:
                """user is holding"""

            if self.managements[index].status is not None:
                managements[index].status = self.managements[index].status
            if self.managements[index].auto_publish is not None:
                managements[index].auto_publish = self.managements[index].auto_publish

        return managements

    @transaction.atomic
    def __call__(self):
        post = self.modify_content()
        post_managements = self.modify_exist_managements()

        post.save()
        PostManagement.objects.bulk_update(post_managements, ["status", "auto_publish"])
