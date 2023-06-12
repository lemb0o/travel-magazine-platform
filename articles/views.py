from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.template.defaultfilters import slugify
from django.core.cache import caches
from django.conf import settings
import redis


from .models import Article
from accounts.models import User

from .forms import CreateArticleForm
from multimedia.forms import CreateVideoForm

db_cache = caches['db']
# connect to redis
r = redis.StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


class ArticleList(ListView):
    model = Article
    template_name = 'articles/list_articles.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        context.update({
            'popular_authors': db_cache.get('popular_authors'),
            'popular_articles': db_cache.get('popular_articles'),
            'popular_events': db_cache.get('popular_events')
        })
        return context


class ArticleDetail(DetailView):
    model = Article
    template_name = 'articles/detail_article.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        context.update({
            # increment total image views by 1
            'total_views': r.incr('article:{}:views'.format(self.object.id)),
            'popular_authors': db_cache.get('popular_authors'),
            'popular_articles': db_cache.get('popular_articles'),
            'popular_events': db_cache.get('popular_events')

        })
        # increment Author ranking by 1
        r.zincrby('author_ranking', self.object.user.id, 1)
        # increment article ranking by 1
        r.zincrby('article_ranking', self.object.id, 1)
        return context


@method_decorator(user_passes_test(lambda u: u.groups.filter(name='Authors').exists() or u.is_superuser),
                  name='dispatch')
class ArticleDelete(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('articles:ArticleList')


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='Authors').exists() or u.is_superuser)
def create_article(request):
    form = CreateArticleForm(request.POST or None, request.FILES or None)
    form2 = CreateVideoForm(request.POST or None, request.FILES or None)
    if form.is_valid() and form2.is_valid():
        article = form.save(commit=False)
        article.user = User.objects.get(pk=request.user.pk)
        article.slug = slugify(article.title)
        article.save()
        return HttpResponseRedirect("/articles/{article.pk}/update/")
    #                                                           context_instance=RequestContext(request))
    return render(request, 'articles/create_article.html', {'form': form, 'form2': form2})


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='Authors').exists() or u.is_superuser)
def update_article(request, pk):
    article = get_object_or_404(Article, id=pk)
    form = CreateArticleForm(request.POST or None, request.FILES or None, instance=article)
    # vid_form = CreateVideoForm(request.POST or None, request.FILES or None)
    if form.is_valid(): # vid_form.is_valid()
        if form.has_changed():
            form.save()
            return HttpResponseRedirect("/articles/{pk}/update")
        # print(form1.errors, form2.errors)
    return render(request, 'articles/update_article.html',
                  {'form': form})


# if img_form.has_changed():
#     img_form.changed_data
#     for img in request.FILES.getlist('image'):
#         update_image(img=img, target=article, target_img_name='articles/imgs/')
# if vid_form.has_changed():
#     for vid in request.FILES.getlist('video'):
#         create_video(vid=vid, target=article, target_vid_name='articles/vids/')

# @login_required()
# def create_article(request):
#     if request.method == 'GET':
#         form1 = CreateArticleForm()
#         form2 = CreateImageForm()
#         form3 = CreateVideoForm()
#     if request.method == 'POST':
#         form1 = CreateArticleForm(request.POST)
#         form2 = CreateImageForm(request.POST, request.FILES)
#         form3 = CreateVideoForm(request.POST, request.FILES)
#         if form1.is_valid() and form2.is_valid() and form3.is_valid():
#             article = form1.save(commit=False)
#             article.user = User.objects.get(pk=request.user.pk)
#             article.save()
#             for img in request.FILES.getlist('image'):
#                 create_image(img=img, target=article, target_img_name='articles/imgs/')
#             for vid in request.FILES.getlist('video'):
#                 create_video(vid=vid, target=article, target_vid_name='articles/vids/')
#             return HttpResponseRedirect("/articles/")
#         # print(form1.errors, form2.errors)
#         else:
#             form1 = CreateArticleForm(request.POST)
#             form2 = CreateImageForm(request.POST, request.FILES)
#             form3 = CreateVideoForm(request.POST, request.FILES)
#     return render(request, 'articles/create_article.html',
#                   {'form1': form1, 'form2': form2, 'form3': form3}, )  # context_instance=RequestContext(request))
