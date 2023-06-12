from __future__ import absolute_import, unicode_literals
# from celery.schedules import crontab
# from gemspedia.celery import app
from celery import task

from django.db.models import Count
from datetime import datetime, timedelta
from django.core.cache import caches
from .models import Event

db_cache = caches['db']


@task()
def task_cache_popular_events():
    now = datetime.now()
    return db_cache.set(
        'popular_events', Event.get_upcoming_events(
            start=now.date(), end=now.date() + timedelta(days=15)
        ).annotate(
            users_num=Count('users')
        ).order_by('-users_num')[:5],
        None  # this's the expire time. setting it to None to make it permanent.
    )
