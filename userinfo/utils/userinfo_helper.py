__author__ = 'nliu'

from userinfo.models import UserInfo


class UserInfoHelper(object):
    def __init__(self):
        pass

    def get_user_info(self, user_id):
        try:
            row = UserInfo.objects.get(user_id=user_id)
            img_url = row.img_url
            gender = row.img_url
            nickname = row.nickname
            info = dict(
                user_id=user_id,
                nickname=nickname,
                img_url=img_url,
                gender=gender,
            )
        except UserInfo.DoesNotExist:
            info = dict()
        return info

    def get_user_info_list(self, user_id_list):
        user_info_list = []
        for row in UserInfo.objects.filter(user_id__in=user_id_list):
            user_info_list.append(dict(
                user_id=row.user_id,
                nickname=row.nickname,
                img_url=row.img_url,
                gender=row.gender
            ))
        return user_info_list