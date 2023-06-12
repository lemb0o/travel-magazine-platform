from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from accounts.models import User
from multimedia.models import Video

from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import ugettext_lazy as _
from common.miscellaneous import get_file_path


# Create your models here.
class Article(models.Model):
    user = models.ForeignKey(User, related_name='created_articles')
    cover_img = models.ImageField(upload_to=get_file_path(file_dir='articles-cover-imgs/'))
    videos = GenericRelation(Video, related_query_name='article')
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=100, unique=True)
    description = RichTextUploadingField(max_length=2200)
    created = models.DateTimeField(_('Time Created'), auto_now_add=True)  # add current date.
    updated = models.DateTimeField(_('Time Updated'), auto_now=True)  # update date.

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title
