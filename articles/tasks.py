from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab
from magazine.celery import app
from celery import task

from django.core.cache import caches
from django.conf import settings
from accounts.models import User
from .models import Article
import redis


db_cache = caches['db']
# connect to redis
r = redis.StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


@task()
def task_cache_popular_articles():
    article_ranking = r.zrange('article_ranking', 1, -1, desc=True)[:5]
    article_ranking_ids = [int(i) for i in article_ranking]
    # get most viewed articles
    most_viewed = list(Article.objects.filter(id__in=article_ranking_ids))
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))
    db_cache.set('popular_articles', most_viewed, None)


@task()
def task_cache_popular_authors():
    author_ranking = r.zrange('author_ranking', 0, -1, desc=True)[:4]
    author_ranking_ids = [int(i) for i in author_ranking]
    # get most viewed articles
    most_viewed = list(User.objects.filter(id__in=author_ranking_ids))
    most_viewed.sort(key=lambda x: author_ranking_ids.index(x.id))
    db_cache.set('popular_authors', most_viewed, None)


# app.conf.beat_schedule = {
#     # Executes every Monday morning at 7:30 a.m.
#     'cache-popular-articles': {
#         'task': 'articles.tasks.task_cache_popular_articles',
#         'schedule': crontab(minute=4),
#     },
# }
# # articles periodic tasks.
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls task_cache_popular_articles() every 3 hours.
#     sender.add_periodic_task(
#         crontab(minute=8), task_cache_popular_articles.s(), name='cache popular articles every 3 hours'
#     )
#
#     # Calls task_cache_popular_authors() every 12 hours.
#     sender.add_periodic_task(
#         crontab(minute=12), task_cache_popular_articles.s(), name='cache popular authors every 12 hours'
#     )
