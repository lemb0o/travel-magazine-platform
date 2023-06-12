from django.db import models
from accounts.models import User
from travels.models import Travel
from events.models import Event


# Create your models here.
class AbstractReservation(models.Model):
    charge_id = models.CharField(blank=True, max_length=256)
    tickets = models.PositiveSmallIntegerField()
    paid = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)

    class Meta:
        abstract = True


class EventReservation(AbstractReservation):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_reservations')
    event = models.ForeignKey(Event, related_name='reservations')


class TravelReservation(AbstractReservation):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='travels_reservations')
    event = models.ForeignKey(Travel, related_name='reservations')
