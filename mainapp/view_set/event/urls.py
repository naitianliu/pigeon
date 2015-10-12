__author__ = 'nliu'

from django.conf.urls import patterns, url

urlpatterns = patterns('mainapp.view_set.event',

    url(r'^task/create/$', 'task.create_task'),
    url(r'^task/invite_members/$', 'task.invite_members_to_task'),
    url(r'^task/accept/$', 'task.accept_task'),
    url(r'^task/reject/$', 'task.reject_task'),
    url(r'^task/exit/$', 'task.exit_task'),

    url(r'^topic/create/$', 'topic.create_topic'),
    url(r'^topic/invite_members/$', 'topic.invite_members_to_topic'),
    url(r'^topic/exit/$', 'topic.exit_topic'),

    url(r'^reminder/create/$', 'reminder.create_reminder'),
    url(r'^reminder/change_receivers/$', 'reminder.change_receivers'),
    url(r'^reminder/complete/$', 'reminder.complete_reminder_by_receiver'),
    url(r'^reminder/revoke/$', 'reminder.revoke_reminder_by_creator'),
    url(r'^reminder/delay/$', 'reminder.delay_reminder_by_receiver'),
    url(r'^reminder/reject/$', 'reminder.reject_reminder_by_receiver'),
    url(r'^reminder/resend/$', 'reminder.resend_reminder_by_creator'),

    url(r'^activity/create/$', 'activity.create_activity'),
    url(r'^activity/invite_members/$', 'activity.invite_members_to_activity'),
    url(r'^activity/exit/$', 'activity.exit_activity'),
    url(r'^activity/notify/$', 'activity.post_notification'),

    url(r'^list/updated_events/$', 'list_events.get_all_updated_events_list'),
    url(r'^list/event_info/$', 'list_events.get_event_info'),

)