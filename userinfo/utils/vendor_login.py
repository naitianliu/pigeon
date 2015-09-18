__author__ = 'nliu'

from userinfo.vendors.weibo_api import WeiboAPI
from userinfo.models import UserInfo, Vendor
import time

'''vendor type: wb, wx, qq'''


class VendorLogin(object):
    def __init__(self, vendor_type, vendor_id, access_token):
        self.vendor_type = vendor_type
        self.vendor_id = vendor_id
        self.access_token = access_token
        self.current_time = int(time.time())

    def login(self):
        if self.vendor_type == 'wb':
            user_info = WeiboAPI().get_user_info(self.access_token, self.vendor_id)
        else:
            user_info = {}
        if user_info:
            user_id = user_info['user_id']
            nickname = user_info['nickname']
            img_url = user_info['profile_img_url']
            gender = user_info['gender']
            try:
                Vendor.objects.get(vendor_id=self.vendor_id, vendor_type=self.vendor_type)
            except Vendor.DoesNotExist:
                Vendor(
                    user_id=user_id,
                    vendor_id=self.vendor_id,
                    vendor_type=self.vendor_type,
                    is_active=True
                ).save()
            try:
                row = UserInfo.objects.get(user_id=user_id)
                row.img_url = img_url,
                row.gender = gender,
                row.nickname = nickname
                row.is_active = True,
                row.last_login_time = self.current_time
                row.save()
            except UserInfo.DoesNotExist:
                UserInfo(
                    user_id=user_id,
                    img_url=img_url,
                    gender=gender,
                    nickname=nickname,
                    is_active=True,
                    created_time=self.current_time,
                    last_login_time=self.current_time
                ).save()
            return user_id
        else:
            return ""