from django.contrib import admin
from user.models import UserInfo, Passcode


# Register your models here.

admin.site.register(UserInfo)
admin.site.register(Passcode)
