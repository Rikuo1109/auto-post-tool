from django.contrib import admin

from .models import ImagePost


@admin.register(ImagePost)
class ImagePostAdmin(admin.ModelAdmin):
    pass
