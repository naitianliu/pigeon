__author__ = 'nliu'

from django.conf.urls import patterns, url

urlpatterns = patterns('mainapp.view_set.event',

    url(r'^task/create/$', 'task.create_task'),
    url(r'^task/invite_members/$', 'task.invite_members_to_task'),
    url(r'^task/accept/$', 'task.accept_task'),
    url(r'^task/reject/$', 'task.reject_task'),
    url(r'^task/exit/$', 'task.exit_task'),

    url(r'^topic/create/$', 'topic.create_topic'),

    url(r'^reminder/create/$', 'reminder.create_reminder'),

    url(r'^activity/create/$', 'activity.create_activity'),

)