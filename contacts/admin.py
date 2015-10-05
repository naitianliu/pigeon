from django.contrib import admin
from contacts.models import Person
from contacts.models import Group

# Register your models here.

admin.site.register(Person)
admin.site.register(Group)

