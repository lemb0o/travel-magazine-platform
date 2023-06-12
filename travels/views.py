from datetime import datetime, timedelta
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.core.cache import caches

from .models import Travel
from accounts.models import User

from .forms import CreateTravelForm
from multimedia.forms import CreateImageForm, CreateVideoForm
from multimedia.utils import create_image, create_video

db_cache = caches['db']


# Create your views here.
class TravelList(ListView):
    model = Travel
    template_name = 'travels/list_travels.html'
    context_object_name = 'travels'
    queryset = Travel.objects.filter(start__date__gte=datetime.now().date())

    def get_context_data(self, **kwargs):
        context = super(TravelList, self).get_context_data(**kwargs)
        context.update({
            'popular_authors': db_cache.get('popular_authors'),
            'popular_articles': db_cache.get('popular_articles'),
            'popular_events': db_cache.get('popular_events')
        })
        return context


class TravelDetail(DetailView):
    model = Travel
    template_name = 'travels/detail_travel.html'
    context_object_name = 'travel'

    def get_context_data(self, **kwargs):
        context = super(TravelDetail, self).get_context_data(**kwargs)
        context.update({
            'popular_authors': db_cache.get('popular_authors'),
            'popular_articles': db_cache.get('popular_articles'),
            'popular_events': db_cache.get('popular_events')
        })
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser or u.is_staff), name='dispatch')
class TravelDelete(LoginRequiredMixin, DeleteView):
    model = Travel
    success_url = reverse_lazy('travels:TravelList')


@login_required()
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def create_travel(request):
    form1 = CreateTravelForm(request.POST or None)
    form2 = CreateImageForm(request.POST or None, request.FILES or None)
    form3 = CreateVideoForm(request.POST or None, request.FILES or None)
    if form1.is_valid() and form2.is_valid() and form3.is_valid():
        travel = form1.save(commit=False)
        travel.user = User.objects.get(pk=request.user.pk)
        travel.save()
        for img in request.FILES.getlist('image'):
            create_image(img=img, target=travel, target_img_name='travels/imgs/')
        for vid in request.FILES.getlist('video'):
            create_video(vid=vid, target=travel, target_vid_name='travels/vids/')
        return HttpResponseRedirect("/travels/{travel.pk}/update/")
    return render(request, 'travels/create_travel.html',
                  {'form1': form1, 'form2': form2, 'form3': form3})


@login_required()
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def update_travel(request, pk):
    travel = get_object_or_404(Travel, id=pk)
    form = CreateTravelForm(request.POST or None, instance=travel)
    # vid_form = CreateVideoForm(request.POST or None, request.FILES or None)
    if form.is_valid(): # vid_form.is_valid()
        if form.has_changed():
            form.save()
            return HttpResponseRedirect("/travels/{pk}/update")
        # print(form1.errors, form2.errors)
    return render(request, 'travels/update_travel.html',
                  {'form': form})


# if img_form.has_changed():
#     img_form.changed_data
#     for img in request.FILES.getlist('image'):
#         update_image(img=img, target=travel, target_img_name='travels/imgs/')
# if vid_form.has_changed():
#     for vid in request.FILES.getlist('video'):
#         create_video(vid=vid, target=travel, target_vid_name='travels/vids/')
