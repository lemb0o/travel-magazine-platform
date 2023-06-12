from django.conf.urls import url
from .views import (
    TravelList, TravelDetail, create_travel, TravelDelete, update_travel
)

urlpatterns = [
    url(r'^$', TravelList.as_view(), name='TravelList'),
    url(r'^(?P<pk>[\d]+)/$', TravelDetail.as_view(), name='TravelDetail'),
    url(r'^(?P<pk>[\d]+)/delete/$', TravelDelete.as_view(), name='TravelDelete'),
    url(r'^(?P<pk>[\d]+)/update/$', update_travel, name='TravelUpdate'),
    url(r'^create/$', create_travel, name='TravelCreate'),
]

