__author__ = 'nliu'

from contacts.models import Person
from userinfo.models import UserInfo
from userinfo.utils.userinfo_helper import UserInfoHelper


class PersonHelper(object):
    def __init__(self, user_id):
        self.user_id = user_id

    def get_friend_list(self):
        friend_id_list = []
        for row in Person.objects.filter(requester_id=self.user_id, status='complete'):
            friend_id_list.append(row.receiver_id)
        for row in Person.objects.filter(receiver_id=self.user_id, status='complete'):
            friend_id_list.append(row.requester_id)
        friend_info_list = UserInfoHelper().get_user_info_list(friend_id_list)
        return friend_info_list

    def display_user_list_by_keyword(self, keyword):
        user_list_by_id = []
        user_list_by_nickname = []
        for row in UserInfo.objects.filter(user_id=keyword):
            user_list_by_id.append(dict(
                user_id=row.user_id,
                nickname=row.nickname,
                img_url=row.img_url
            ))
        for row in UserInfo.objects.filter(nickname=keyword):
            user_list_by_nickname.append(dict(
                user_id=row.user_id,
                nickname=row.nickname,
                img_url=row.img_url
            ))
        result_dict = dict(
            user_list_by_id=user_list_by_id,
            user_list_by_nickname=user_list_by_nickname
        )
        return result_dict

    def send_friend_request(self, receiver_id):
        try:
            row = Person.objects.get(requester_id=self.user_id, receiver_id=receiver_id)
            status = row.status
            if status == 'pending':
                error = "already sent request"
            elif status == 'complete':
                error = "you are friend already"
            else:
                error = ""
            result_dict = dict(error=error)
        except Person.DoesNotExist:
            Person(
                requester_id=self.user_id,
                receiver_id=receiver_id,
                status='pending',
            ).save()
            result_dict = dict(result="success")
        return result_dict

    def get_pending_friend_request_list(self):
        sent_requests_list = []
        waiting_requests_list = []
        for row in Person.objects.filter(requester_id=self.user_id, status='pending'):
            sent_requests_list.append(dict(
                requester_id=row.requester_id,
                receiver_id=row.receiver_id
            ))
        for row in Person.objects.filter(receiver_id=self.user_id, status='pending'):
            waiting_requests_list.append(dict(
                requester_id=row.requester_id,
                receiver_id=row.receiver_id
            ))
        result_dict = dict(
            sent_requests_list=sent_requests_list,
            waiting_requests_list=waiting_requests_list
        )
        return result_dict

    def accept_friend_request(self, requester_id):
        try:
            row = Person.objects.get(requester_id=requester_id, receiver_id=self.user_id)
            row.status = 'complete'
            row.save()
            result_dict = dict(result='success')
        except Person.DoesNotExist:
            error = "invalid. no request exists"
            result_dict = dict(error=error)
        return result_dict

    def deny_friend_request(self, requester_id):
        try:
            row = Person.objects.get(requester_id=requester_id, receiver_id=self.user_id)
            row.delete()
            result_dict = dict(result='success')
        except Person.DoesNotExist:
            error = "invalid. no request exists"
            result_dict = dict(error=error)
        return result_dict

    def delete_friend(self, friend_id):
        try:
            row = Person.objects.get(requester_id=friend_id, receiver_id=self.user_id)
            row.delete()
            result_dict = dict(result="success")
        except Person.DoesNotExist:
            try:
                row = Person.objects.get(requester_id=self.user_id, receiver_id=friend_id)
                row.delete()
                result_dict = dict(result="success")
            except Person.DoesNotExist:
                error = "relationship does not exist"
                result_dict = dict(error=error)
        return result_dict