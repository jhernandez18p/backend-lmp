from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.safestring import mark_safe


from .models import Car, SubType, Transmission, Fuel
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
        'model',
        'brand',
        'year',
        'sub_type',
        'price',
        'status',
        'views',
    ]

    list_display_links = [
        'model',
    ]

    list_editable = [
        'brand',
        'year',
        'sub_type',
        'price',
        'status',
    ]
    list_filter = [
        'brand',
        'model',
        'sub_type',
        'status',

    ]
    search_fields = [
        'brand',
        'model',
        'year',
        'description',
        'status',
    ]
    
    # fieldsets = [
    #     (_('Author'), {'fields': ['author','']}),
    #     ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    # ]

    readonly_fields = ["imagen_principal_del_carro"]

    def imagen_principal_del_carro(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.img.url,
            width=obj.img.width / 3,
            height=obj.img.height / 3,
        )
    )

    inlines = [PhotoInline]
    
    class Meta:
        model = Car


admin.site.register(Car, CarModelAdmin)
admin.site.register(SubType)
admin.site.register(Fuel)
admin.site.register(Transmission)