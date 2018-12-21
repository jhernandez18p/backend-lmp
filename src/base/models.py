from __future__ import unicode_literals

import os
import random
from datetime import datetime

from django.db import models
from django.contrib.flatpages.models import FlatPage
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

class Position(models.Model):
    name = models.CharField(max_length=144, blank=True,verbose_name = _('Nombre'))
    description = RichTextField(blank=True, verbose_name = _('Descripción'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Posición")
        verbose_name_plural = _("Posiciones")


class Pages(models.Model):
    name = models.CharField(max_length=144, blank=True,verbose_name = _('Nombre'))
    description = RichTextField(blank=True, verbose_name = _('Descripción'))
    have_icon = models.BooleanField(default=False,verbose_name = _('¿Usa icono?'))
    url = models.CharField(max_length=18, blank=True, null=True,verbose_name = _('Dirección url'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Página")
        verbose_name_plural = _("Paginas")


class Carousel(models.Model):
    name = models.CharField(max_length=144, blank=True,verbose_name = _('Nombre'))
    description = RichTextField(blank=True, verbose_name = _('Descripción'))
    page = models.ForeignKey(Pages, default=1, on_delete=models.CASCADE,blank=True,verbose_name = _('Página asociada'))
    position = models.ForeignKey(Position, default=1, on_delete=models.CASCADE,blank=True,verbose_name = _('Posición asociada'))
    crated_at = models.DateTimeField(auto_now=True,verbose_name = _('¿Cuando fue creado?'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Carousel")
        verbose_name_plural = _("Carousel")


class CarouselImage(models.Model):
    Carousel = models.ForeignKey(Carousel, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_path,verbose_name = _('Imágen'))
    name = models.CharField(max_length=144, blank=True,verbose_name = _('Nombre'))
    text = RichTextField(blank=True, verbose_name = _('Testo para mostrar sobre la imágen'))
    call_to_action_url = models.ForeignKey(
        FlatPage, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        verbose_name = _('Llamado a acción')
    )
    uploaded_at = models.DateTimeField(auto_now=True,verbose_name = _('¿Cuando fue creado?'))
    
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Imágen del carousel")
        verbose_name_plural = _("Imagenes del carousel")


class Site(models.Model):

    name = models.CharField(max_length = 140, blank=True,verbose_name = _('Nombre'))
    title = models.CharField(max_length=144, blank=True, null=True,verbose_name = _('Título'))
    description = RichTextField( blank=True, verbose_name = _('Descripción'))
    short_description = RichTextField( blank=True, verbose_name = _('Descripción corta'), max_length=240)
    url = models.CharField(max_length = 140, blank=True,verbose_name = _('Dirección URL'))
    phone = models.CharField(max_length=144, blank=True, null=True,verbose_name = _('Número de teléfono principal'))
    phone2 = models.CharField(max_length=144, blank=True, null=True,verbose_name = _('Número de teléfono secundario'))
    email = models.CharField(max_length=144, blank=True, null=True,verbose_name = _('Correo electronico principal'))
    email2 = models.CharField(max_length=144, blank=True, null=True,verbose_name = _('Correo electronico secundario'))
    schedule = models.CharField(max_length=144, blank=True, null=True,verbose_name = _('Horario de atención'))
    schedule2 = models.CharField(max_length=144, blank=True, null=True,verbose_name = _('Horario de atención 2'))
    workday = models.CharField(max_length=144, blank=True, null=True,verbose_name = _('Días laborales'))
    address = models.CharField(max_length=144, blank=True, null=True,verbose_name = _('Dirección principal'))
    address1 = models.CharField(max_length=144, blank=True, null=True,verbose_name = _('Dirección secundaria'))
    logo = models.ImageField(null=True, blank=True, upload_to=get_upload_path, verbose_name = _('Logo del sitio'))
    site_img = models.ImageField(null=True, blank=True, upload_to=get_upload_path, verbose_name = _('Imágen destacada'))
    services_img = models.ImageField(null=True, blank=True, upload_to=get_upload_path, verbose_name = _('Imágen para servicios'))
    products_img = models.ImageField(null=True, blank=True, upload_to=get_upload_path, verbose_name = _('Imágen para productos'))
    is_undercostruction = models.BooleanField( default=False,verbose_name = _('en construcción'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Informacion del sitio')
        verbose_name_plural = _('Informacion del sitio')


class SocialMedia(models.Model):

    ICON_CHOICES = (
        ('fa-500px','500px'),
        ('fa-amazon','Amazon'),
        ('fa-cc-amex','Amex'),
        ('fa-angellist','Angellist'),
        ('fa-behance','Behanse'),
        ('fa-behance','Behanse'),
        ('fa-behance-square','Behanse1'),
        ('fa-bitbucket','Bitbucket'),
        ('fa-bitbucket-square','Bitbucket1'),
        ('fa-btc','BitCoin'),
        ('fa-buysellads','Buysellads'),
        ('fa-codepen ','Codepen'),
        ('fa-digg','Digg'),
        ('fa-cc-diners-club','Dinners Clud'),
        ('fa-cc-discover','Discover'),
        ('fa-dribbble','Dribble'),
        ('fa-dropbox','Dropbox'),
        ('fa-facebook','Facebook'),
        ('fa-facebook','Facebook'),
        ('fa-facebook-square','Facebook1'),
        ('fa-facebook-official','Facebook2'),
        ('fa-github','GitHub'),
        ('fa-github-alt ','GitHub1'),
        ('fa-github-square','GitHub2'),
        ('fa-gitlab','GitLab'),
        ('fa-google-wallet ','Google Wallet'),
        ('fa-google','Google'),
        ('fa-google-plus','Google+'),
        ('fa-google-plus-square','Google+1'),
        ('fa-google-plus-official','Google+2'),
        ('fa-hacker-news','Hacker News'),
        ('fa-instagram','Instagram'),
        ('fa-cc-jcb','JCB'),
        ('fa-jsfiddle','JsFiddle'),
        ('fa-linkedin','LinkedIn'),
        ('fa-linkedin-square','LinkedIn1'),
        ('fa-cc-mastercard ','MasterCard'),
        ('fa-medium','Medium'),
        ('fa-meetup','Meetup'),
        ('fa-opencart','Opencart'),
        ('fa-cc-paypal','Paypal'),
        ('fa-paypal','Paypal'),
        ('fa-pinterest','Printerest'),
        ('fa-pinterest-square','Printerest1'),
        ('fa-pinterest-p','Printerest2'),
        ('fa-quora','Quora'),
        ('fa-reddit','Reddit'),
        ('fa-reddit-square','Reddit1'),
        ('fa-reddit-alien','Reddit2'),
        ('fa-skype','Skype'),
        ('fa-slack','Slack'),
        ('fa-slideshare','Slideshare'),
        ('fa-snapchat','Snapchat'),
        ('fa-snapchat-square','Snapchat1'),
        ('fa-snapchat-ghost','Snapchat2'),
        ('fa-soundcloud','Soundcloud'),
        ('fa-spotify','Spotify'),
        ('fa-stack-overflow ','Stack Overflow'),
        ('fa-cc-stripe','Stripe'),
        ('fa-telegram','Telegram'),
        ('fa-trello','Trello'),
        ('fa-tripadvisor','Tripadvisor'),
        ('fa-tumblr','Tumblr'),
        ('fa-tumblr-square','Tumblr1'),
        ('fa-twitch','Twitch'),
        ('fa-twitter','Twitter'),
        ('fa-twitter-square','Twitter1'),
        ('fa-usb','USB'),
        ('fa-viacoin','Viacoin'),
        ('fa-vimeo-square','Vimeo'),
        ('fa-vine','Vine'),
        ('fa-cc-visa','Visa'),
        ('fa-weixin','Weixin'),
        ('fa-whatsapp','Whatsapp'),
        ('fa-wikipedia-w','Wikipedia'),
        ('fa-windows','Windows'),
        ('fa-wordpress','Wordpress'),
        ('fa-wpbeginner','WPBeguinner'),
        ('fa-wpforms','WpForms'),
        ('fa-xing-square','Xing Square'),
        ('fa-xing','Xing'),
        ('fa-y-combinator','Y Combinator'),
        ('fa-yahoo','Yahoo'),
        ('fa-yelp','Yelp'),
        ('fa-youtube','YouTube'),
        ('fa-youtube-square','YouTube1'),
        ('fa-youtube-play','YouTube2'),
    )

    site = models.ForeignKey(Site, related_name='Social_Media', on_delete=models.CASCADE)
    name = models.CharField(max_length = 1444, blank=True,verbose_name = _('Nombre'))
    url = models.CharField(max_length = 1444, blank=True,verbose_name = _('Dirección url'))
    icon = models.CharField(max_length = 1444, blank=True,verbose_name = _('Icono'), choices=ICON_CHOICES,)
    title = models.CharField(max_length = 1444, blank=True,verbose_name = _('Titulo'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Perfiles de redes sociales')
        verbose_name_plural = _('Perfiles de redes sociales')


class Widget(models.Model):
    name = models.CharField(max_length=144, blank=True,verbose_name = _('Nombre'))
    description = RichTextField(blank=True, verbose_name = _('Descripción'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Widget")
        verbose_name_plural = _("Widgets")