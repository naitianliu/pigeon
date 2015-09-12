__author__ = 'nliu'

from mainapp.db_api import aws_api
from mainapp.models import EventPost
import time
import uuid


class PostHelper(object):
    def __init__(self, user_id):
        self.__current_time = int(time.time())
        self.user_id = user_id

    def create_new_post(self, event_id, post_info):
        post_info['created_time'] = self.__current_time
        post_id = str(uuid.uuid1())
        aws_api.Post().create(post_id, post_info)
        EventPost(
            event_id=event_id,
            post_id=post_id,
            user_id=self.user_id,
            created_time=self.__current_time
        ).save()

    def get_post_list_by_event_id(self, event_id, from_time=None, to_time=None):
        post_id_list = []
        if not from_time:
            from_time = 0
        if not to_time:
            to_time = self.__current_time
        for row in EventPost.objects.filter(event_id=event_id, created_time__gte=from_time, created_time__lte=to_time):
            post_id_list.append(row.post_id)
            if len(post_id_list) >= 20:
                break
        post_info_list = aws_api.Post().batch_query(post_id_list)
        return post_info_list

    def get_post_list_by_user_id(self, from_time=None, to_time=None):
        post_id_list = []
        if not from_time:
            from_time = 0
        if not to_time:
            to_time = self.__current_time
        for row in EventPost.objects.filter(user_id=self.user_id, created_time__gte=from_time, created_time__lte=to_time):
            post_id_list.append(row.post_id)
            if len(post_id_list) >= 20:
                break
        post_info_list = aws_api.Post().batch_query(post_id_list)
        return post_info_list