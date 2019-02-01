from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from src.base.views import Home, About, Inventory, contact, FAQ, booking, trade_in, CarDetail, quotations, sell

app_name = 'front'
urlpatterns = [
    path('', Home.as_view(), name="home" ),
    path('quienes-somos', About.as_view(), name="about" ),
    path('inventario', Inventory.as_view(), name="inventory" ),
    path('detalles/<slug:slug>', CarDetail.as_view(), name='car_detail'),
    path('contacto', contact, name="contact" ),
    path('contacto/f-a-q', FAQ.as_view(), name="contact-f-a-q" ),
    path('contacto/agendar-visita', booking, name="contact-book" ),
    path('contacto/cotizar', quotations, name="contact-quote" ),
    path('contacto/trade-in', trade_in, name="contact-trade-in" ),
    path('contacto/vende-tu-cehiculo', sell, name="sell" ),
]
