from django.conf.urls import url
from .views import (
    ArticleList, ArticleDetail, create_article, ArticleDelete, update_article
)

urlpatterns = [
    url(r'^$', ArticleList.as_view(), name='ArticleList'),
    url(r'^create/$', create_article, name='ArticleCreate'),
    url(r'^(?P<slug>[\w-]+)/$', ArticleDetail.as_view(), name='ArticleDetail'),
    url(r'^(?P<pk>[\d]+)/delete/$', ArticleDelete.as_view(), name='ArticleDelete'),
    url(r'^(?P<pk>[\d]+)/update/$', update_article, name='ArticleUpdate'),
]

