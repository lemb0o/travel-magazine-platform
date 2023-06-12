from datetime import datetime
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.core.cache import caches
from django.conf import settings

from .models import Event
from accounts.models import User

from .forms import CreateEventForm
from multimedia.forms import CreateImageForm, CreateVideoForm
from multimedia.utils import create_image, create_video

db_cache = caches['db']


# Create your views here.
class EventList(ListView):
    model = Event
    queryset = Event.objects.filter(start__date__gte=datetime.now().date())
    template_name = 'events/list_events.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super(EventList, self).get_context_data(**kwargs)
        context.update({
            'popular_authors': db_cache.get('popular_authors'),
            'popular_articles': db_cache.get('popular_articles'),
            'popular_events': db_cache.get('popular_events'),
            'api_key': settings.STRIPE_PUBLIC_KEY,
        })
        return context


class EventDetail(DetailView):
    model = Event
    template_name = 'events/detail_event.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        context.update({
            'popular_authors': db_cache.get('popular_authors'),
            'popular_articles': db_cache.get('popular_articles'),
            'popular_events': db_cache.get('popular_events')
        })
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser or u.is_staff), name='dispatch')
class EventDelete(LoginRequiredMixin, DeleteView):
    model = Event
    success_url = reverse_lazy('events:EventList')


@login_required()
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def create_event(request):
    form1 = CreateEventForm(request.POST or None)
    form2 = CreateImageForm(request.POST or None, request.FILES or None)
    form3 = CreateVideoForm(request.POST or None, request.FILES or None)
    if form1.is_valid() and form2.is_valid() and form3.is_valid():
        event = form1.save(commit=False)
        event.user = User.objects.get(pk=request.user.pk)
        event.save()
        for img in request.FILES.getlist('image'):
            create_image(img=img, target=event, target_img_name='events/imgs/')
        for vid in request.FILES.getlist('video'):
            create_video(vid=vid, target=event, target_vid_name='events/vids/')
        return HttpResponseRedirect("/events/{event.pk}/update/")
    return render(request, 'events/create_event.html',
                  {'form1': form1, 'form2': form2, 'form3': form3})


@login_required()
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def update_event(request, pk):
    event = get_object_or_404(Event, id=pk)
    form = CreateEventForm(request.POST or None, instance=event)
    # vid_form = CreateVideoForm(request.POST or None, request.FILES or None)
    if form.is_valid(): # vid_form.is_valid()
        if form.has_changed():
            form.save()
            return HttpResponseRedirect("/events/{pk}/update")
        # print(form1.errors, form2.errors)
    return render(request, 'events/update_event.html',
                  {'form': form})


@login_required()
def join_event(request, pk):
    print('is this view even work?')
    event = get_object_or_404(Event, id=pk)
    has_reservation = event.reservations.filter(user=request.user, event=event).exists()
    tickets = int(request.POST.get('tickets', 1))
    if not event.price and not has_reservation:
        event.users.add(request.user)
        event.reservations.create(user=request.user, event=event, tickets=tickets)
        event.available_seats -= tickets
        event.save()
        print('done join free')
        messages.success(request, 'you have successfully joined the event.', extra_tags='success')
    elif event.price and not has_reservation:
        description = "reserved {tickets} tickets for {request.user.username}."
        charged = event.charge(request.data['stripeToken'], description, request.user, tickets=tickets)
        print('before charged check')
        if charged:
            event.users.add(request.user)
            event.available_seats -= tickets
            event.save()
            print('done join non free')
            messages.success(request, 'you have successfully joined the event.', extra_tags='success')
        messages.error(request, 'error while charging the user, please try again.', extra_tags='alert')
    elif has_reservation:
        print('already have reservation.')
        messages.warning(request, 'action not permitted, you already made a reservation.', extra_tags='warning')
        return EventList.as_view()(request)
    return render(request, 'events/detail_event.html', {'event': event})


# if img_form.has_changed():
#     img_form.changed_data
#     for img in request.FILES.getlist('image'):
#         update_image(img=img, target=event, target_img_name='events/imgs/')
# if vid_form.has_changed():
#     for vid in request.FILES.getlist('video'):
#         create_video(vid=vid, target=event, target_vid_name='events/vids/')
