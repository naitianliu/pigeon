__author__ = 'nliu'

from boto.dynamodb2.table import Table


class Event(object):
    def __init__(self):
        self.table = Table('Event')
        self.table_post = Table('Post')
        self.table_comment = Table('Comment')

    def create_new_event(self, event_id, event_info):
        self.table.put_item(data=dict(
            event_id=event_id,
            info=event_info
        ))

    def get_event_info_by_event_id(self, event_id):
        event = self.table.get_item(event_id=event_id)
        event_info = event['info']
        return event_info

    def update_event_info_by_event_id(self, event_id, event_info):
        event = self.table.get_item(event_id=event_id)
        event['info'] = event_info
        event.save()

    def batch_query_by_event_id_list(self, event_id_list):
        keys = []
        for event_id in event_id_list:
            keys.append(dict(
                event_id=event_id
            ))
        many_events = self.table.batch_get(keys=keys)
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
    event_id = 0
    event_id_list = []
    event_id_list = map(str, range(1, 11))
    print event_id_list
    event_info_list = obj.batch_query_by_event_id_list(event_id_list)
    print event_info_list
