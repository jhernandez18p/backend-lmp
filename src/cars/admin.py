from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Car
from src.medias.models import Photo, Video


class PhotoInline(GenericTabularInline):
    model = Photo
    extra = 3
    max_num = 15


class VideoInline(GenericTabularInline):
    model = Video
    max_num = 1


class CarModelAdmin(admin.ModelAdmin):
    list_display = [
        'brand',
        'model',
        'milage',
        'year',
        'direction',
        'sub_type',
        'traction',
        'transmission',
        'color',
        'fuel',
        'engine',
        'price',
        'slug',
        'description',
        'status',
        'views',
    ]

    list_display_links = [
        'model',
    ]

    list_editable = [
        'brand',
        'milage',
        'year',
        'direction',
        'sub_type',
        'traction',
        'transmission',
        'color',
        'fuel',
        'engine',
        'price',
        'slug',
        'description',
        'status',
        'views',

    ]
    list_filter = [
        'brand',
        'model',
        'milage',
        'year',
        'direction',
        'sub_type',
        'traction',
        'transmission',
        'color',
        'fuel',
        'engine',
        'price',
        'slug',
        'description',
        'status',
        'views',

    ]
    search_fields = [
        'brand',
        'model',
        'milage',
        'year',
        'direction',
        'sub_type',
        'traction',
        'transmission',
        'color',
        'fuel',
        'engine',
        'price',
        'slug',
        'description',
        'status',
        'views',
    ]
    
    # fieldsets = [
    #     (_('Author'), {'fields': ['author','']}),
    #     ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    # ]
    inlines = [PhotoInline, VideoInline]
    
    class Meta:
        model = Car


admin.site.register(Car, CarModelAdmin)