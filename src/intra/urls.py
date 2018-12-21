from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path

from src.intra.views.base import *

app_name = 'intra'
urlpatterns = [
    path('', Home.as_view(), name='home'),
]