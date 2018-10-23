from __future__ import unicode_literals

from django.contrib import admin

from .models import Photo, Video

admin.site.register(Photo)
admin.site.register(Video)