from django.contrib import admin
from .models import LoginToken, ThirdPartyToken, ResetToken


# Register your models here.
@admin.register(LoginToken)
class LoginTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(ThirdPartyToken)
class ThirdPartyTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(ResetToken)
class ResetTokenAdmin(admin.ModelAdmin):
    pass
