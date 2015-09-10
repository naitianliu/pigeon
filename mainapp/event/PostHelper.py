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
        pass

    def get_post_list_by_user_id(self, user_id, from_time=None, to_time=None):
        pass