from django.contrib import admin

from .models import LoginToken, ResetToken, FacebookToken, TwitterToken, ZaloToken, LinkedInToken


# Register your models here.
@admin.register(LoginToken)
class LoginTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(ResetToken)
class ResetTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(FacebookToken)
class FacebookTokenAdmin(admin.ModelAdmin):
    pass
