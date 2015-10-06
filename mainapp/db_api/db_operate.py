__author__ = 'nliu'

from mainapp.models import UserEvent
from mainapp.models import Comment
import time


class EventDBOperation(object):
    def __init__(self):
        self.__current_time = int(time.time())

    def bulk_create_new_event_per_user(self, event_id, event_type, user_id_list):
        bulk_list = []
        for user_id in user_id_list:
            bulk_list.append(UserEvent(
                user_id=user_id,
                event_id=event_id,
                event_type=event_type,
                is_complete=False,
                is_updated=True,
                created_time=self.__current_time
            ))
        UserEvent.objects.bulk_create(bulk_list)

    def save_comment_by_event_id(self, event_id, content):
        Comment(
            event_id=event_id,
            content=content,
            created_time=self.__current_time
        ).save()

    def get_comments_by_event_id_list(self, event_id_list):
        comments_dict = dict()
        for row in Comment.objects.filter(event_id__in=event_id_list):
            event_id = row.event_id
            if event_id in comments_dict:
                comments_dict[event_id].append(dict(
                    content=row.content,
                    time=row.created_time
                ))
            else:
                comments_dict[event_id] = [dict(
                    content=row.content,
                    time=row.created_time
                )]
        return comments_dict

    def remove_event_per_user(self, event_id, user_id):
        UserEvent.objects.filter(event_id=event_id, user_id=user_id).delete()

    def remove_event_by_user_id_list(self, event_id, user_id_list):
        UserEvent.objects.filter(event_id=event_id, user_id__in=user_id_list).delete()

    def update_event_to_new(self, event_id, target_user_id_list=None):
        if target_user_id_list:
            UserEvent.objects.filter(event_id=event_id, user_id__in=target_user_id_list).update(is_updated=True)
        else:
            UserEvent.objects.filter(event_id=event_id).update(is_updated=True)

    def get_updated_event_id_list(self, user_id):
        event_id_list = []
        for row in UserEvent.objects.filter(user_id=user_id, is_updated=True):
            event_id_list.append(row.event_id)
        return event_id_list
