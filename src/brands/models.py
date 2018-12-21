from __future__ import unicode_literals

import os
import random
from datetime import datetime

from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from ckeditor.fields import RichTextField

def get_upload_path(instance, filename):
    _filename = filename.split('.')
    _filename_ext = _filename[-1]
    _filename_name = ''.join(random.choice(_filename[0]) for _ in range(5))
    filename = '%s.%s' % (_filename_name,_filename_ext)
    try:
        a = instance.name.lower()
    except:
        a = 'lmp'
    final_path = os.path.join('brand/%s/' % (a.lower()), datetime.now().date().strftime("%Y/%m/%d"), filename)
    print(final_path)
    return final_path


def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
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

class Brand(models.Model):
    """
    Modelo de datos para las marcas
    """
    name = models.CharField(max_length=140, blank=True)
    slug = models.CharField(max_length=140, blank=True)
    alt = models.CharField(max_length=140, blank=True)
    count = models.PositiveSmallIntegerField(default=0)
    img = models.ImageField(
        verbose_name=_('Foto'),
        upload_to=get_upload_path,
        blank=True,
        default='/brands/lmp.jpg',
    )
    is_active = models.BooleanField(default=False)

    def update_count(self):
        self.count = Car.objects.all().filter(brand=self.id).count()
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Marca')
        verbose_name_plural = _('Marcas')

pre_save.connect(pre_save_receiver, sender=Brand)