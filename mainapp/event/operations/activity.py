__author__ = 'nliu'

from boto.dynamodb2.table import Table
from mainapp.event.db_operate import EventDBOperation
import time

EVENT_TYPE = "activity"


class ActivityOperation(object):
    def __init__(self, user_id, event_id):
        self.__user_id = user_id
        self.__event_id = event_id
        self.table = Table('Event')
        self.event_item = self.table.get_item(event_id=event_id)
        self.db_event = EventDBOperation()

    def invite_members_to_activity(self, members):
        current_members = self.event_item['info']['members']
        new_members = current_members + members
        self.event_item['info']['members'] = new_members
        self.event_item.partial_save()
        self.db_event.bulk_create_new_event_per_user(self.__event_id, EVENT_TYPE, members)
        self.db_event.update_event_to_new(self.__event_id)

    def exit_topic(self):
        members = self.event_item['info']['members']
        if self.__user_id in members:
            members.remove(self.__user_id)
        self.event_item['info']['members'] = members
        self.event_item.partial_save()
        self.db_event.remove_event_per_user(self.__event_id, self.__user_id)

    def post_notification(self, notification_content):
        members = self.event_item['info']['members']
        current_time = int(time.time())
        temp_list = self.event_item['info']['notification_list']
        temp_list.append(dict(
            created_time=current_time,
            content=notification_content,
            editor_id=self.__user_id
        ))
        self.event_item['info']['notification_list'] = temp_list
        self.event_item.partial_save()
        return members
