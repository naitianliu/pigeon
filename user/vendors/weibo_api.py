__author__ = 'nliu'

import urllib2
import json
from config import URL


class WeiboAPI(object):
    def __init__(self):
        self.url_dict = URL['weibo']

    def get_user_info(self, access_token, uid):
        url = self.url_dict['user_info'] % (access_token, uid)
        try:
            res_dict = json.loads(urllib2.urlopen(url).read())
            user_info = dict(
                user_id="wb%s" % uid,
                nickname=res_dict['screen_name'],
                profile_img_url=res_dict['profile_image_url'],
                gender=res_dict['gender'],
                vendor="wb"
            )
        except urllib2.HTTPError:
            user_info = None
        return user_info
