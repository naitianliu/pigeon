__author__ = 'nliu'

from boto.dynamodb2.table import Table
from mainapp.event.db_operate import EventDBOperation

EVENT_TYPE = "topic"


class TopicOperation(object):
    def __init__(self, user_id, event_id):
        self.__user_id = user_id
        self.__event_id = event_id
        self.table = Table('Event')
        self.event_item = self.table.get_item(event_id=event_id)
        self.db_event = EventDBOperation()

    def invite_members_to_topic(self, members):
        current_members = self.event_item['info']['members']
        new_members = current_members + members
        topic_name = self.event_item['info']['topic_name']
        self.event_item['info']['members'] = new_members
        self.event_item.partial_save()
        self.db_event.bulk_create_new_event_per_user(self.__event_id, EVENT_TYPE, members)
        self.db_event.update_event_to_new(self.__event_id)
        return topic_name

    def exit_topic(self):
        members = self.event_item['info']['members']
        if self.__user_id in members:
            members.remove(self.__user_id)
        self.event_item['info']['members'] = members
        self.event_item.partial_save()
        self.db_event.remove_event_per_user(self.__event_id, self.__user_id)