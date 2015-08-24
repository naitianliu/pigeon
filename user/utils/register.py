__author__ = 'nliu'

from user.models import User
from user.models import Passcode
from django.core.mail import send_mail
from django.contrib.auth.models import User as django_user
import datetime
import random


class UserRegisterHelper(object):
    def __init__(self):
        self.current_time = datetime.datetime.now()

    def register_new_user_by_email(self, vendor_id, vendor_type, password):
        try:
            User.objects.get(vendor_id=vendor_id, vendor_type=vendor_type)
        except User.DoesNotExist:
            self.__auth_register(vendor_id, password)
            img_url = ""
            nickname = vendor_id
            User(
                vendor_id=vendor_id,
                vendor_type=vendor_type,
                user_id=vendor_id,
                img_url=img_url,
                nickname=nickname,
                is_active=False,
                created_time=self.current_time,
                last_login_time=self.current_time
            ).save()
            self.__send_validation_passcode(vendor_id, vendor_id)

    def verify_passcode(self, user_id, passcode):
        try:
            row = User.objects.get(user_id=user_id)
            is_active = row.is_active
        except User.DoesNotExist:
            is_active = False
        try:
            row = Passcode.objects.get(user_id=user_id, passcode=passcode)
            result = passcode == row.passcode and not is_active
        except Passcode.DoesNotExist:
            result = False
        return result

    def generate_token(self):
        pass

    def __auth_register(self, username, password):
        user = django_user.objects.create_user(username, email=None, password=password)
        user.save()

    def __send_validation_passcode(self, user_id, email):
        passcode_generated = "%d" % random.randrange(100000, 999999)
        try:
            row = Passcode.objects.get(user_id=user_id)
            row.passcode = passcode_generated
            row.save()
        except Passcode.DoesNotExist:
            Passcode(
                user_id=user_id,
                passcode=passcode_generated,
            ).save()
        self.__send_email(email, passcode_generated)

    def __send_email(self, email, content):
        send_mail(subject="title", message=content, from_email='Pigeon <naitianliu@gmail.com>', recipient_list=[email])

    def resend_validation_passcode(self, user_id):
        self.__send_validation_passcode(user_id, user_id)

    def test_send_email(self, email, content):
        self.__send_email(email, content)