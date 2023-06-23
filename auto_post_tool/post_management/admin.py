from django.contrib import admin

from .models import Post, PostManagement


@admin.register(PostManagement)
class PostManagementAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass
