from django.db import models

# Create your models here.


class Person(models.Model):
    requester_id = models.CharField(max_length=100)
    receiver_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    created_time = models.DateTimeField(auto_now=True, auto_created=True)


class Group(models.Model):
    group_id = models.CharField
    group_name = models.CharField(max_length=100)
    creator_id = models.CharField(max_length=100)
    member_id = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_created=True, auto_now=True)