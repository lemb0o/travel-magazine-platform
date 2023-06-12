from django.contrib import admin
from .models import Image, Video

# Register your models here.
admin.site.register([Image, Video])
