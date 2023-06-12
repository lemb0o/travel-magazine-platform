from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.core.cache import caches

from .models import Place
from accounts.models import User

from .forms import CreatePlaceForm
from multimedia.forms import CreateImageForm, CreateVideoForm
from multimedia.utils import create_image, create_video

db_cache = caches['db']


# Create your views here.
class PlaceList(ListView):
    model = Place
    template_name = 'places/list_places.html'
    context_object_name = 'places'

    def get_context_data(self, **kwargs):
        context = super(PlaceList, self).get_context_data(**kwargs)
        context.update({
            'popular_authors': db_cache.get('popular_authors'),
            'popular_articles': db_cache.get('popular_articles'),
            'popular_events': db_cache.get('popular_events')
        })
        return context


class PlaceDetail(DetailView):
    model = Place
    template_name = 'places/detail_place.html'
    context_object_name = 'place'

    def get_context_data(self, **kwargs):
        context = super(PlaceDetail, self).get_context_data(**kwargs)
        context.update({
            'popular_authors': db_cache.get('popular_authors'),
            'popular_articles': db_cache.get('popular_articles'),
            'popular_events': db_cache.get('popular_events')
        })
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser or u.is_staff), name='dispatch')
class PlaceDelete(LoginRequiredMixin, DeleteView):
    model = Place
    success_url = reverse_lazy('places:PlaceList')


@login_required()
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def create_place(request):
    form1 = CreatePlaceForm(request.POST or None)
    form2 = CreateImageForm(request.POST or None, request.FILES or None)
    form3 = CreateVideoForm(request.POST or None, request.FILES or None)
    if form1.is_valid() and form2.is_valid() and form3.is_valid():
        place = form1.save(commit=False)
        place.user = User.objects.get(pk=request.user.pk)
        place.save()
        for img in request.FILES.getlist('image'):
            create_image(img=img, target=place, target_img_name='places/imgs/')
        for vid in request.FILES.getlist('video'):
            create_video(vid=vid, target=place, target_vid_name='places/vids/')
        return HttpResponseRedirect("/places/{place.pk}/update/")
    return render(request, 'places/create_place.html',
                  {'form1': form1, 'form2': form2, 'form3': form3})


@login_required()
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def update_place(request, pk):
    place = get_object_or_404(Place, id=pk)
    form = CreatePlaceForm(request.POST or None, instance=place)
    # vid_form = CreateVideoForm(request.POST or None, request.FILES or None)
    if form.is_valid(): # vid_form.is_valid()
        if form.has_changed():
            form.save()
            return HttpResponseRedirect("/places/{pk}/update")
        # print(form1.errors, form2.errors)
    return render(request, 'places/update_place.html',
                  {'form': form})
