from django.conf.urls import url
from .views import (
    EventList, EventDetail, create_event, EventDelete, update_event, join_event
)

urlpatterns = [
    url(r'^$', EventList.as_view(), name='EventList'),
    url(r'^(?P<pk>[\d]+)/$', EventDetail.as_view(), name='EventDetail'),
    url(r'^(?P<pk>[\d]+)/delete/$', EventDelete.as_view(), name='EventDelete'),
    url(r'^(?P<pk>[\d]+)/update/$', update_event, name='EventUpdate'),
    url(r'^create/$', create_event, name='EventCreate'),
    url(r'^(?P<pk>[\d]+)/join/$', join_event, name='EventJoin'),
]

