from django.urls import reverse
from src.base.models import (Pages,Position,Site,SocialMedia)
from src.users.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail

from src.users.models import Profile
from src.brands.models import Brand
from src.cars.models import Car

def site(request):
    """
    Site info preprocessor 
    """
    context = {}
    context['SITE_TITLE'] = 'Luxury Motors Panamá'
    context['SITE_URL'] = 'https://www.luxurymotorspanama.com/'
    context['SITE_LOGO'] = '/static/base/images/logo.png'

    # pages = Pages.objects.all()
    # if not pages.exists():
    #     new_pages = [
    #         {'name':'Inicio','url':'/','have_icon':False},
    #         {'name':'¿Quienes somos?','url':'quienes-somos','have_icon':False},
    #         {'name':'Inventario','url':'inventario','have_icon':False},
    #         {'name':'Contacto','url':reverse('front:contact'),'have_icon':False},
    #     ]
    #     for object_list in new_pages:
    #         new_page = Pages(
    #             name=object_list['name'],
    #             url=object_list['url'],
    #             have_icon=object_list['have_icon']
    #         )
    #         new_page.save()

    # positions = Position.objects.all()
    # if not positions.exists():
    #     default_positions = [
    #         {'name':'header','description':''},
    #         {'name':'body','description':''},
    #         {'name':'footer','description':''},
    #     ]
    #     for object_list in default_positions:
    #         new_position = Position(
    #             name=object_list['name'],
    #             description=object_list['description'],
    #         )
    #         new_position.save()

    # info_site = Site.objects.filter(id=1)
    # if info_site.exists():
    #     context['info_site'] = info_site[0]
    #     sm = SocialMedia.objects.filter(site=info_site[0].id)
    #     if sm.exists():
    #         context['social_media'] = sm
    # else:
    #     info_site = Site(
    #         name='Luxury Motors Panamá',
    #         description='',
    #         url='https://www.luxurymotorspanama.com',
    #     )
    #     info_site.save()
    
    return context

def brands(request):
    """
    Brands preprocessor 
    """
    context = {}

    brands = Brand.objects.all()
    if brands.exists():
        context['brand_list'] = brands
        context['brand_list_footer'] = brands.order_by('?')[:5]

    return context


def top_cars(request):
    """
    Tot 5 cars preprocessor 
    """
    context = {}

    cars = Car.objects.all().order_by('views')
    if cars.exists():
        context['top_five_cars'] = cars[:5]

    return context