__author__ = 'nliu'

from mainapp.db_api import aws_api
from mainapp.models import UserEvent
import uuid
import time


class EventHelper(object):
    def __init__(self):
        self.__current_time = int(time.time())

    def create_new_event(self, event_info, user_id_list):
        event_info['created_time'] = self.__current_time
        event_id = str(uuid.uuid1())
        aws_api.Event().create_new_event(event_id, event_info)
        bulk_list = []
        for user_id in user_id_list:
            bulk_list.append(UserEvent(
                user_id=user_id,
                event_id=event_id,
                is_complete=False,
                created_time=self.__current_time
            ))
        UserEvent.objects.bulk_create(bulk_list)

    def get_event_list_by_user_id(self, user_id, from_time=None, to_time=None):
        event_id_list = []
        if not from_time:
            from_time = 0
        if not to_time:
            to_time = self.__current_time
        for row in UserEvent.objects.filter(user_id=user_id, is_complete=False, created_time__gte=from_time, created_time__lte=to_time):
            event_id_list.append(row.event_id)
            if len(event_id_list) >= 20:
                break
        event_info_list = aws_api.Event().batch_query_by_event_id_list(event_id_list)

        return event_info_list

    def add_remove_members(self, event_id, user_id, new_member_list):
        """creator action"""
        pass

    def exit_from_event(self, event_id, user_id):
        """member action"""
        pass
