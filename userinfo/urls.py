__author__ = 'nliu'


from django.conf.urls import patterns, url

urlpatterns = patterns('userinfo.views',

    url(r'^$', 'user'),
    url(r'^register/$', 'user_register'),
    url(r'^verify_passcode/$', 'verify_passcode'),
    url(r'^login/$', 'login'),
    url(r'^logout/$', 'logout'),
    url(r'^vendor_login/$', 'vendor_login'),

    url(r'^test/$', 'test'),
)