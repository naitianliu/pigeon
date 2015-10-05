__author__ = 'nliu'

from mainapp.db_api import aws_api
from mainapp.models import UserEvent
import uuid
import time


class CreateEventHelper(object):
    def __init__(self, user_id, event_type):
        self.__creator_id = user_id
        self.__event_type = event_type
        self.__current_time = int(time.time())
        self.__event_id = str(uuid.uuid1())

    def create_task(self, name, description, todo_list, members, time_dict, location_dict):
        event_info = dict(
            creator_id=self.__creator_id,
            event_type=self.__event_type,
            created_time=self.__current_time,
            task_name=name,
            task_description=description,
            todo_list=todo_list,
            members=members,
            time=time_dict,
            location=location_dict
        )
        self.__create(event_info, members)
        return self.__event_id

    def create_topic(self, name, description, members):
        event_info = dict(
            creator_id=self.__creator_id,
            event_type=self.__event_type,
            created_time=self.__current_time,
            topic_name=name,
            topic_description=description,
            members=members
        )
        self.__create(event_info, members)
        return self.__event_id

    def create_reminder(self, content, receivers, time_dict, location_dict):
        event_info = dict(
            creator_id=self.__creator_id,
            event_type=self.__event_type,
            created_time=self.__current_time,
            reminder_content=content,
            receivers=receivers,
            time_dict=time_dict,
            location_dict=location_dict
        )
        self.__create(event_info, receivers)
        return self.__event_id

    def create_activity(self, description, members, time_dict, location_dict):
        event_info = dict(
            creator_id=self.__creator_id,
            event_type=self.__event_type,
            created_time=self.__current_time,
            activity_description=description,
            members=members,
            time=time_dict,
            location=location_dict
        )
        self.__create(event_info, members)
        return self.__event_id

    def __create(self, event_info, members):
        aws_api.Event().create_new_event(self.__event_id, event_info)
        user_id_list = members + [self.__creator_id]
        bulk_list = []
        for user_id in user_id_list:
            bulk_list.append(UserEvent(
                user_id=user_id,
                event_id=self.__event_id,
                event_type=self.__event_type,
                is_complete=False,
                is_updated=True,
                created_time=self.__current_time
            ))
        UserEvent.objects.bulk_create(bulk_list)