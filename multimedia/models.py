from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Image(models.Model):
    image = models.ImageField(_('images'), upload_to='')
    content_type = models.ForeignKey(ContentType, related_name='target_obj_img')
    object_id = models.PositiveIntegerField(db_index=True)
    target = GenericForeignKey()
    created = models.DateTimeField(_('Time Created'), auto_now_add=True)  # add current date.
    updated = models.DateTimeField(_('Time Updated'), auto_now=True)  # update date.

    class Meta:
        ordering = ['-created']


class Video(models.Model):
    video = models.FileField(_('videos'), upload_to='')
    content_type = models.ForeignKey(ContentType, related_name='target_obj_vid')
    object_id = models.PositiveIntegerField(db_index=True)
    target = GenericForeignKey()
    created = models.DateTimeField(_('Time Created'), auto_now_add=True)  # add current date.
    updated = models.DateTimeField(_('Time Updated'), auto_now=True)  # update date.

    class Meta:
        ordering = ['-created']