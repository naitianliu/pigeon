__author__ = 'nliu'

from mainapp.db_api import aws_api
from mainapp.models import PostComment
import time
import uuid


class CommentHelper(object):
    def __init__(self, user_id):
        self.__current_time = int(time.time())
        self.user_id = user_id

    def create_new_comment(self, post_id, comment_info):
        comment_info['created_time'] = self.__current_time
        comment_id = str(uuid.uuid1())
        aws_api.Comment().create(comment_id, comment_info)
        PostComment(
            post_id=post_id,
            comment_id=comment_id,
            user_id=self.user_id,
            created_time=self.__current_time
        ).save()

    def get_comment_list_by_post_id(self, post_id, from_time=None, to_time=None):
        comment_id_list = []
        if not from_time:
            from_time = 0
        if not to_time:
            to_time = self.__current_time
        for row in PostComment.objects.filter(post_id=post_id, created_time__gte=from_time, created_time__lte=to_time):
            comment_id_list.append(row.comment_id)
            if len(comment_id_list) >= 20:
                break
        comment_info_list = aws_api.Comment().batch_query(comment_id_list)
        return comment_info_list