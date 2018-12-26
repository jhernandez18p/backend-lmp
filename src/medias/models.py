from __future__ import unicode_literals

import os
import random
from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from ckeditor.fields import RichTextField

# from src.cars.models import Car


def get_upload_path(instance, filename):
    _filename = filename.split('.')
    _filename_ext = _filename[-1]
    _filename_name = ''.join(random.choice(_filename[0]) for _ in range(5))
    filename = '%s.%s' % (_filename_name,_filename_ext)
    print(filename)
    try:
        a = instance.alt.lower()
    except:
        a = 'lmp'
    return os.path.join('medias/%s/' % (a.lower()), datetime.now().date().strftime("%Y/%m/%d"), filename)


class Photo(models.Model):
    """
    Modelo de datos para las fotos
    """
    img = models.ImageField(
        upload_to=get_upload_path,
        # null=True,
        blank=True,
        default='photos/lmp.jpg',
    )
    category = models.CharField(max_length=144, blank=True)
    alt = models.CharField(max_length=144, blank=True)
    position = models.PositiveSmallIntegerField(default=0)
    featured = models.BooleanField(default=False)
    # car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name=_('Carro'))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,verbose_name=_('Tipo de contenido'))
    content_object = GenericForeignKey('content_type', 'object_id')
    object_id = models.PositiveIntegerField(verbose_name=_('Id de relación'))

    def __str__(self):
        return self.alt

    class Meta:
        verbose_name = _('Foto')
        verbose_name_plural = _('Fotos')


class Video(models.Model):
    """
    Modelo de datos para los videos
    """
    name = models.CharField(max_length=140, blank=True)
    url = models.CharField(max_length=140, blank=True)
    alt = models.CharField(max_length=140, blank=True)
    # car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name=_('Carro'))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,verbose_name=_('Tipo de contenido'))
    content_object = GenericForeignKey('content_type', 'object_id')
    object_id = models.PositiveIntegerField(verbose_name=_('Id de relación'))
    img = models.ImageField(
        upload_to=get_upload_path,
        null=True,
        blank=True,
        default='/videos/lmp.jpg',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')