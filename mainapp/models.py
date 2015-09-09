from django.db import models

# Create your models here.


class UserEvent(models.Model):
    user_id = models.CharField(max_length=100)
    event_id = models.CharField(max_length=50)
    is_complete = models.BooleanField()
    created_time = models.IntegerField()