__author__ = 'nliu'

from django.conf.urls import patterns, url

urlpatterns = patterns('contacts.views',

    url(r'^person/get_friend_list/$', 'person_get_friend_list'),
    url(r'^person/display_user_list_by_keyword/$', 'person_display_user_list_by_keyword'),
    url(r'^person/send_friend_request/$', 'person_send_friend_request'),
    url(r'^person/get_pending_friend_request_list/$', 'person_get_pending_friend_request_list'),
    url(r'^person/accept_friend_request/$', 'person_accept_friend_request'),
    url(r'^person/deny_friend_request/$', 'person_deny_friend_request'),
    url(r'^person/delete_friend/$', 'person_delete_friend'),

    url(r'^group/get_group_list/$', 'group_get_group_list'),
    url(r'^group/create_new_group/$', 'group_create_new_group'),
    url(r'^group/edit_group/$', 'group_edit_group'),
    url(r'^group/delete_group/$', 'group_delete_group'),

)