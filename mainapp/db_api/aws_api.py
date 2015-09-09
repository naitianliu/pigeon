__author__ = 'nliu'

from boto.dynamodb2.table import Table
import boto.dynamodb2
from boto.dynamodb2.items import Item
import config


class Event(object):
    def __init__(self):
        conn = boto.dynamodb2.connect_to_region('us-east-1', )
        self.table_event = Table('Event')

    def create_new_event(self, event_id, event_info):
        print(event_id)
        data = dict(
            event_id=event_id,
            info=event_info
        )
        self.table_event.put_item(data=data)
        # Item(self.table, data=data).save()

    def get_event_info_by_event_id(self, event_id):
        event = self.table_event.get_item(event_id=event_id)
        event_info = event['info']
        return event_info

    def update_event_info_by_event_id(self, event_id, event_info):
        event = self.table_event.get_item(event_id=event_id)
        event['info'] = event_info
        event.save()

    def batch_query_by_event_id_list(self, event_id_list):
        keys = []
        for event_id in event_id_list:
            keys.append(dict(
                event_id=event_id
            ))
        many_events = self.table_event.batch_get(keys=keys)
        event_info_list = []
        for event in many_events:
            event_info_list.append(event['info'])
        return event_info_list


class UserActivity(object):
    def __init__(self):
        self.table = Table('UserActivity')


class Post(object):
    def __init__(self):
        self.table = Table('Post')


class Comment(object):
    def __init__(self):
        self.table = Table('Comment')


if __name__ == '__main__':
    obj = Event()
    event_id = "32eaa4c0-56c2-11e5-b1a4-6003089edb3c12"
    event_info = {
        "description": "description",
        "location": "location",
        "address": "address",
        "time": 1234,
        "members": ["wb2525851962"]
    }
    Event().create_new_event(event_id, event_info)
