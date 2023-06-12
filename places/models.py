from django.db import models
from multimedia.models import Image, Video

from common.miscellaneous import get_file_path
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor.fields import RichTextField


# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextField(max_length=1024)
    location = models.CharField(max_length=255)
    cover_img = models.ImageField(upload_to=get_file_path(file_dir='places-cover-imgs/'))
    images = GenericRelation(Image, related_query_name='places')
    videos = GenericRelation(Video, related_query_name='places')
    created = models.DateTimeField(_('Time Created'), auto_now_add=True, editable=True)  # add current date.
    updated = models.DateTimeField(_('Time Updated'), auto_now=True, editable=True)  # update date.

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

    # image = models.ImageField(
    #     _('image'),
    #     # at initial migration change get_file_path to "places/img/" to prevent errors.
    #     upload_to=get_file_path(file_dir="places/img/"),
    # )
    # video = models.FileField(
    #     _('video'), blank=True, null=True,
    #     # at initial migration change get_file_path to "places/vid/" to prevent errors.
    #     upload_to=get_file_path(file_dir="places/vid/"),
    # )