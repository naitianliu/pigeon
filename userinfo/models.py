from django.db import models

# Create your models here.


class UserInfo(models.Model):
    user_id = models.CharField(max_length=100)
    img_url = models.TextField()
    gender = models.CharField(max_length=1)
    nickname = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_created=True)
    last_login_time = models.IntegerField()

    def __unicode__(self):
        return self.user_id


class Vendor(models.Model):
    user_id = models.CharField(max_length=100)
    vendor_id = models.CharField(max_length=100)
    vendor_type = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now=True)


class Passcode(models.Model):
    user_id = models.CharField(max_length=50)
    passcode = models.CharField(max_length=20)
    created_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user_id