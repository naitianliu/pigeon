__author__ = 'nliu'


from django.conf.urls import patterns, url

urlpatterns = patterns('mainapp.views',

    url(r'^create_new_event/$', 'create_new_event'),
    url(r'^get_event_list/$', 'get_event_list'),

    url(r'^create_new_post/$', 'create_new_post'),
    url(r'^get_post_list/$', 'get_post_list'),

)