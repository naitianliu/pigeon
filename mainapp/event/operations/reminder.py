__author__ = 'nliu'

from boto.dynamodb2.table import Table

from mainapp.db_api.db_operate import EventDBOperation

EVENT_TYPE = "reminder"


class ReminderOperation(object):
    def __init__(self, user_id, event_id):
        self.__user_id = user_id
        self.__event_id = event_id
        self.table = Table('Event')
        self.event_item = self.table.get_item(event_id=event_id)
        self.db_event = EventDBOperation()

    def change_receivers(self, receivers):
        current_receivers = self.event_item['info']['receivers']
        self.event_item['info']['receivers'] = receivers
        self.event_item['info']['receiver_status'] = dict.fromkeys(receivers, 0)
        self.event_item.partial_save()
        self.db_event.remove_event_by_user_id_list(self.__event_id, current_receivers)
        self.db_event.bulk_create_new_event_per_user(self.__event_id, EVENT_TYPE, receivers)
        self.db_event.update_event_to_new(self.__event_id)

    def complete_reminder_by_receiver(self, message=None):
        creator_id = self.event_item['info']['creator_id']
        self.event_item['info']['receiver_status'][self.__user_id] = 1
        self.event_item.partial_save()
        self.db_event.save_comment_by_event_id(self.__event_id, self.__user_id, action=1, content=message)
        self.db_event.update_event_to_new(self.__event_id)
        return creator_id

    def revoke_reminder_by_creator(self, message=None):
        creator_id = self.event_item['info']['creator_id']
        receivers = self.event_item['info']['receivers']
        self.event_item['info']['status'] = 5
        self.event_item.partial_save()
        self.db_event.save_comment_by_event_id(self.__event_id, self.__user_id, action=5, content=message)
        user_id_list = receivers + [self.__user_id]
        self.db_event.remove_event_per_user(self.__event_id, user_id_list)
        return creator_id

    def delay_reminder_by_receiver(self, message=None):
        creator_id = self.event_item['info']['creator_id']
        self.event_item['info']['receiver_status'][self.__user_id] = 2
        self.event_item.partial_save()
        self.db_event.save_comment_by_event_id(self.__event_id, self.__user_id, action=2, content=message)
        self.db_event.update_event_to_new(self.__event_id)
        return creator_id

    def reject_reminder_by_receiver(self, message=None):
        creator_id = self.event_item['info']['creator_id']
        self.event_item['info']['receiver_status'][self.__user_id] = 3
        self.event_item.partial_save()
        self.db_event.save_comment_by_event_id(self.__event_id, self.__user_id, action=3, content=message)
        self.db_event.update_event_to_new(self.__event_id)
        self.db_event.remove_event_per_user(self.__event_id, self.__user_id)
        return creator_id

    def resend_reminder_by_creator(self, message=None):
        creator_id = self.event_item['info']['creator_id']
        self.event_item['info']['status'] = 6
        self.event_item.partial_save()
        self.db_event.save_comment_by_event_id(self.__event_id, self.__user_id, action=6, content=message)
        self.db_event.update_event_to_new(self.__event_id)
        return creator_id