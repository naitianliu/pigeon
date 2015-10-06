__author__ = 'nliu'

from boto.dynamodb2.table import Table
from mainapp.db_api.aws_api import Event
from mainapp.db_api.db_operate import EventDBOperation


class ListEventsHelper(object):
    def __init__(self, user_id):
        self.__user_id = user_id
        self.db_event = EventDBOperation()
        self.aws_event = Event()

    def get_all_updated_events_list(self):
        event_id_list = self.db_event.get_updated_event_id_list(self.__user_id)
        comments_dict = self.db_event.get_comments_by_event_id_list(event_id_list)
        print(comments_dict)
        event_info_list = self.aws_event.batch_query_by_event_id_list(event_id_list)
        result_list = []
        for event_info in event_info_list:
            event_id = event_info['event_id']
            if event_id in comments_dict:
                comments = comments_dict[event_id]
            else:
                comments = []
            result_list.append(dict(
                event_id=event_id,
                info=event_info['info'],
                comments=comments
            ))
        return result_list

    def get_all_pending_events_list(self):
        pass

    def get_all_events_by_page(self):
        pass

    def get_event_info(self, event_id):
        event_info = self.aws_event.get_event_info_by_event_id(event_id)
        comments_dict = self.db_event.get_comments_by_event_id_list([event_id])
        if event_id in comments_dict:
            comments = comments_dict[event_id]
        else:
            comments = []
        result_dict = dict(
            event_id=event_id,
            info=event_info,
            comments=comments
        )
        return result_dict