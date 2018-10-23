from __future__ import unicode_literals

import os
import random

from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from ckeditor.fields import RichTextField
from src.brands.models import Brand
from src.medias.models import Photo, Video


def create_slug(instance, new_slug=None):
    slug = slugify('%s-%s-%s'%(instance.brand.name, instance.model, instance.year))
    if new_slug is not None:
        slug = new_slug
    qs = instance.__class__.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug or instance.slug == '':
        instance.slug = create_slug(instance)

class Car(models.Model):
    """
    Modelo de datos para los carros
    """
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.CharField(max_length=140, blank=True)
    milage = models.CharField(max_length=140, blank=True)
    year = models.CharField(max_length=140, blank=True)
    direction = models.CharField(max_length=140, blank=True)
    sub_type = models.CharField(max_length=140, blank=True)
    traction = models.CharField(max_length=140, blank=True)
    transmission = models.CharField(max_length=140, blank=True)
    color = models.CharField(max_length=140, blank=True)
    fuel = models.CharField(max_length=140, blank=True)
    engine = models.CharField(max_length=140, blank=True)
    price = models.IntegerField()
    slug = models.CharField(max_length=140, blank=True)
    description = RichTextField(blank=True)
    photos = models.ManyToManyField(Photo, blank=True)
    videos = models.ManyToManyField(Video, blank=True)

    def __str__(self):
        return '%s %s' %( self.model, self.year )

    class Meta:
        verbose_name = _('Carro')
        verbose_name_plural = _('Carros')

pre_save.connect(pre_save_receiver, sender=Car)