from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Site,SocialMedia,Position,Pages,Carousel,\
    CarouselImage,Widget

class SocialMediaInline(admin.StackedInline):
    model = SocialMedia
    extra = 1

class SiteAdmin(admin.ModelAdmin):
    inlines = [SocialMediaInline,]


class CarouselImageInline(admin.StackedInline):
    model = CarouselImage
    extra = 1

class CarouselAdmin(admin.ModelAdmin):
    inlines = [CarouselImageInline,]

# admin.site.register(Position)
# admin.site.register(Pages)
# admin.site.register(Widget)
# admin.site.register(CarouselImage)
admin.site.register(Site, SiteAdmin)
admin.site.register(Carousel, CarouselAdmin)