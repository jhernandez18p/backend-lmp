from __future__ import unicode_literals

import os
import random

from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse

from ckeditor.fields import RichTextField
from src.brands.models import Brand
from src.medias.models import Photo, Video

def get_upload_path(instance, filename):
    
    try:
        a = instance.brand.slug.lower()
        b = slugify(instance.model.lower())
    except:
        a = 'lmp'
        b = 'base'
    
    _filename = filename.split('.')
    _filename_ext = _filename[-1]
    _filename_name = ''.join(random.choice(_filename[0]) for _ in range(5))
    filename = '%s.%s' % (_filename_name,_filename_ext)
    print(filename)
    
    return os.path.join('medias/%s/%s/' % (a, b), filename)

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

class Fuel(models.Model):
    """
    Modelo de datos para el tipo de combustible
    """
    name = models.CharField(max_length=144)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Combustible')
        verbose_name_plural = _('Combustibles')



class Transmission(models.Model):
    """
    Modelo de datos para los tipos de Trnsmisiones 
    """

    name = models.CharField(max_length=144)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Transmisión')
        verbose_name_plural = _('Transmisiones')


class SubType(models.Model):
    """
    Modelo de datos para los tipos de vahículos
    """

    name = models.CharField(max_length=144)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Tipo de vehículo')
        verbose_name_plural = _('Tipos de vehiculos')


class Car(models.Model):
    """
    Modelo de datos para los carros
    """
    SOLD = 'SOLD'
    OUT_STOCK = 'OUT'
    IN_STOCK = 'IN'
    COMING = 'COMING'
    CAR_STATUS_CHOICES = (
        (SOLD, 'Vendido'),
        (OUT_STOCK, 'Agotado'),
        (IN_STOCK, 'Disponible'),
        (COMING, 'Llega proximamente'),
    )
    img = models.ImageField(
        upload_to=get_upload_path,
        # null=True,
        blank=True,
        default='photos/lmp.jpg',
    )
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
    price = models.IntegerField(blank=True, null=True)
    slug = models.CharField(max_length=140, blank=True)
    description = RichTextField(blank=True)
    status = models.CharField('status', max_length=10, choices=CAR_STATUS_CHOICES, default='IN', blank=True)
    views = models.SmallIntegerField(
        default=0,
        blank=True,
        verbose_name=_('Numero de visitas')
    )

    def __str__(self):
        return '%s %s' %( self.model, self.year )

    def get_absolute_url(self):
        return reverse('front:car_detail', kwargs={'slug': self.slug})

    def update_counter(self):
        self.views = self.views + 1
        self.save()

    class Meta:
        ordering = ['brand__name']
        verbose_name = _('Carro')
        verbose_name_plural = _('Carros')



pre_save.connect(pre_save_receiver, sender=Car)