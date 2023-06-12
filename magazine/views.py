from django.shortcuts import render
from datetime import datetime, timedelta
from django.db.models import Count
from django.core.cache import caches

from articles.models import Article
from places.models import Place
from events.models import Event
from travels.models import Travel
from django.contrib.auth.models import Group

db_cache = caches['db']
cache = caches['default']


def home_page(request):
    now = datetime.now()
    articles = Article.objects.all()[:8]
    places = Place.objects.all().order_by('created')[:5]
    # get all events from current day to 2 weeks later.
    events = Event.get_upcoming_events(start=now.date(), end=now.date()+timedelta(days=15))
    db_cache.set(
        'popular_events', events.annotate(users_num=Count('users')).order_by('-users_num')[:4], None  # 3 hours
    )
    travels = Travel.objects.filter(start__date__gte=now.date(), end__date__lte=now.date()+timedelta(days=30))\
        .order_by('start')[:6]
    popular_events = db_cache.get('popular_events')
    popular_authors = db_cache.get('popular_authors')
    popular_articles = db_cache.get('popular_articles')

    return render(request, 'home/index.html', {
        'articles': articles, 'places': places, 'events': events,
        'travels': travels, 'popular_events': popular_events,
        'popular_articles': popular_articles, 'popular_authors': popular_authors,
    })


def privacy(request):
    return render(request, 'account/privacy.html')