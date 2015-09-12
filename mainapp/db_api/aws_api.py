__author__ = 'nliu'

from boto.dynamodb2.table import Table


class Event(object):
    def __init__(self):
        self.table_event = Table('Event')

    def create_new_event(self, event_id, event_info):
        print(event_id)
        data = dict(
            event_id=event_id,
            info=event_info
        )
        self.table_event.put_item(data=data)

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

    def create(self, post_id, post_info):
        data = dict(
            post_id=post_id,
            info=post_info
        )
        self.table.put_item(data=data)

    def get(self, post_id):
        post = self.table.get_item(post_id=post_id)
        post_info = post['info']
        return post_info

    def update(self, post_id, post_info):
        post = self.table.get_item(post_id=post_id)
        post['info'] = post_info
        post.save()

    def batch_query(self, post_id_list):
        keys = []
        for post_id in post_id_list:
            keys.append(dict(
                post_id=post_id
            ))
        many_posts = self.table.batch_get(keys=keys)
        post_info_list = []
        for post in many_posts:
            post_info_list.append(post['info'])
        return post_info_list


class Comment(object):
    def __init__(self):
        self.table = Table('Comment')

    def create(self, comment_id, comment_info):
        data = dict(
            comment_id=comment_id,
            info=comment_info
        )
        self.table.put_item(data=data)

    def get(self, comment_id):
        comment = self.table.get_item(comment_id=comment_id)
        comment_info = comment['info']
        return comment_info

    def update(self, comment_id, comment_info):
        comment = self.table.get_item(comment_id=comment_id)
        comment['info'] = comment_info
        comment.save()

    def batch_query(self, comment_id_list):
        keys = []
        for comment_id in comment_id_list:
            keys.append(dict(
                comment_id=comment_id
            ))
        many_comments = self.table.batch_get(keys=keys)
        comment_info_list = []
        for comment in many_comments:
            comment_info_list.append(comment['info'])
        return comment_info_list


if __name__ == '__main__':
    post_id = "4"
    event_info = {
        "description": "description",
        "location": "location",
        "address": "address",
        "time": 1234,
        "members": ["wb2525851962"]
    }
    print Post().get(post_id)
