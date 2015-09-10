from django.db import models

# Create your models here.


class UserEvent(models.Model):
    user_id = models.CharField(max_length=100)
    event_id = models.CharField(max_length=50)
    is_complete = models.BooleanField()
    created_time = models.IntegerField()


class EventPost(models.Model):
    event_id = models.CharField(max_length=50)
    post_id = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)
    created_time = models.IntegerField()


class PostComment(models.Model):
    post_id = models.CharField(max_length=50)
    comment_id = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)
    created_time = models.IntegerField()