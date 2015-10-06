__author__ = 'nliu'

from boto.dynamodb2.table import Table

from mainapp.db_api.db_operate import EventDBOperation

EVENT_TYPE = "task"


class TaskOperation(object):
    def __init__(self, user_id, event_id):
        self.__user_id = user_id
        self.__event_id = event_id
        self.table = Table('Event')
        self.event_item = self.table.get_item(event_id=event_id)
        self.db_event = EventDBOperation()

    def invite_members_to_task(self, members):
        current_members = self.event_item['info']['members']
        member_status = self.event_item['info']['member_status']
        temp = member_status.copy()
        temp.update(dict.fromkeys(members, 0))
        new_members = current_members + members
        task_name = self.event_item['info']['task_name']
        self.event_item['info']['members'] = new_members
        self.event_item['info']['member_status'] = temp
        self.event_item.partial_save()
        self.db_event.bulk_create_new_event_per_user(self.__event_id, EVENT_TYPE, members)
        return task_name

    def accept_task(self, message=None):
        self.event_item['info']['member_status'][self.__user_id] = 1
        self.event_item.partial_save()
        if message:
            self.db_event.save_comment_by_event_id(self.__event_id, message)
        self.db_event.update_event_to_new(self.__event_id)

    def reject_task(self, message=None):
        self.event_item['info']['member_status'][self.__user_id] = 2
        members = self.event_item['info']['members']
        if self.__user_id in members:
            members.remove(self.__user_id)
        self.event_item['info']['members'] = members
        self.event_item.partial_save()
        self.db_event.remove_event_per_user(self.__event_id, self.__user_id)
        if message:
            self.db_event.save_comment_by_event_id(self.__event_id, message)
        self.db_event.update_event_to_new(self.__event_id)

    def exit_task(self, message=None):
        self.event_item['info']['member_status'][self.__user_id] = 3
        members = self.event_item['info']['members']
        if self.__user_id in members:
            members.remove(self.__user_id)
        self.event_item['info']['members'] = members
        self.event_item.partial_save()
        self.db_event.remove_event_per_user(self.__event_id, self.__user_id)
        if message:
            self.db_event.save_comment_by_event_id(self.__event_id, message)
        self.db_event.update_event_to_new(self.__event_id)