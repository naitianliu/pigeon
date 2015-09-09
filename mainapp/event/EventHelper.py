__author__ = 'nliu'

from mainapp.db_api import aws_api
from mainapp.models import UserEvent
import uuid
import time


class EventHelper(object):
    def __init__(self):
        self.current_time = int(time.time())

    def create_new_event(self, event_info, user_id_list):
        event_info["created_time"] = self.current_time
        event_id = str(uuid.uuid1())
        print(11)
        aws_api.Event().create_new_event(event_id, event_info)
        print(22)
        bulk_list = []
        for user_id in user_id_list:
            bulk_list.append(UserEvent(
                user_id=user_id,
                event_id=event_id,
                is_complete=False,
                created_time=self.current_time
            ))
        UserEvent.objects.bulk_create(bulk_list)

    def get_event_list_by_user_id(self, user_id, from_time=None, to_time=None):
        event_id_list = []
        if not from_time:
            from_time = 0
        if not to_time:
            to_time = self.current_time
        for row in UserEvent.objects.filter(user_id=user_id, is_complete=False, created_time__level__gte=from_time, created_time__level__lte=to_time):
            event_id_list.append(row.event_id)
            if len(event_id_list) >= 20:
                break
        event_info_list = aws_api.Event().batch_query_by_event_id_list(event_id_list)
        return event_info_list
