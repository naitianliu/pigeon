__author__ = 'nliu'

from contacts.models import Group
from userinfo.utils.userinfo_helper import UserInfoHelper
import uuid


class GroupHelper(object):
    def __init__(self, user_id):
        self.user_id = user_id

    def get_group_list(self):
        temp_dict = {}
        for row in Group.objects.filter(creator_id=self.user_id):
            group_id = row.group_id
            if group_id not in temp_dict:
                temp_dict[group_id] = dict(
                    group_id=group_id,
                    group_name=row.group_name,
                    members=[row.member_id]
                )
            else:
                temp_dict[group_id]['members'].append(row.member_id)
        group_info_list = temp_dict.values()
        return group_info_list

    def create_new_group(self, group_name, member_list):
        group_id = str(uuid.uuid1())
        bulk_list = []
        for member_id in member_list:
            bulk_list.append(
                Group(
                    group_id=group_id,
                    group_name=group_name,
                    creator_id=self.user_id,
                    member_id=member_id
                ))
        Group.objects.bulk_create(bulk_list)
        result_dict = dict(result="success")
        return result_dict

    def edit_group(self, group_id, group_name, member_list):
        old_member_list = []
        for row in Group.objects.filter(group_id=group_id, creator_id=self.user_id):
            member_id = row.member_id
            old_member_list.append(member_id)
            if member_id not in member_list:
                row.delete()
        new_add_member_id_list = list(set(member_list) - set(old_member_list))
        bulk_list = []
        for member_id in new_add_member_id_list:
            bulk_list.append(
                Group(
                    group_id=group_id,
                    group_name=group_name,
                    creator_id=self.user_id,
                    member_id=member_id
                ))
        Group.objects.bulk_create(bulk_list)
        result_dict = dict(result="success")
        return result_dict

    def delete_group(self, group_id):
        for row in Group.objects.filter(group_id=group_id, creator_id=self.user_id):
            row.delete()
        result_dict = dict(result="success")
        return result_dict