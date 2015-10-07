from django.db import models

# Create your models here.


class UserEvent(models.Model):
    user_id = models.CharField(max_length=100)
    event_id = models.CharField(max_length=50)
    event_type = models.CharField(max_length=30, default="unknown")
    is_complete = models.BooleanField(default=False)
    is_updated = models.BooleanField(default=True)
    created_time = models.IntegerField()

    def __unicode__(self):
        return self.event_id


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


class Comment(models.Model):
    event_id = models.CharField(max_length=50)
    user_id = models.CharField(max_length=100, default="")
    action = models.IntegerField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    created_time = models.IntegerField()

    def __unicode__(self):
        return self.content