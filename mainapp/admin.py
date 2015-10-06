from django.contrib import admin
from mainapp.models import Comment, UserEvent

# Register your models here.

admin.site.register(Comment)
admin.site.register(UserEvent)
