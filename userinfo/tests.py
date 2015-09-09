from django.test import TestCase

# Create your tests here.

from userinfo.vendors.weibo_api import WeiboAPI


class UserTests(TestCase):
    def test_weibo_get_user_info(self):
        access_token = '2.00mTNwkC6hbjAE6b5dee438colhHzB'
        uid = '2525851962'
        user_info = WeiboAPI().get_user_info(access_token, uid)
        print(user_info)