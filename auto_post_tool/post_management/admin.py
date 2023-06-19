from django.contrib import admin

from .models import PostManagement, Post


@admin.register(PostManagement)
class PostManagementAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass
