from django.conf.urls import url
from django.urls import path, include, re_path

from rest_framework import routers
from rest_framework.authtoken.views import ObtainAuthToken

from src.api.views import UserCreate, \
    CarListByBrand, CarListByPrice, CarListByYear, CarListByModel

from src.api.viewset import UserViewSet, CarViewSet, BrandViewSet, SiteViewSet, \
    PhotoViewSet, VideoViewSet, ProfileViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('profile', ProfileViewSet)
router.register('cars', CarViewSet)
router.register('brands', BrandViewSet)
router.register('site', SiteViewSet)
router.register('photo', PhotoViewSet)
router.register('video', VideoViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('cars/filter/brand/<slug>/', CarListByBrand.as_view(), name='list-cars-by-brand-name'),
    path('cars/filter/model/<slug>/', CarListByModel.as_view(), name='list-cars-by-brand-name'),
    # By Price
    path('cars/filter/price/-<min_price>/', CarListByPrice.as_view(), name='list-cars-by-min-price'),
    path('cars/filter/price/<max_price>/', CarListByPrice.as_view(), name='list-cars-by-max-price'),
    path('cars/filter/price/-<min_price>/<max_price>/', CarListByPrice.as_view(), name='list-cars-by-price'),
    # By Year
    path('cars/filter/year/-<min_year>/', CarListByYear.as_view(), name='list-cars-by-min-year'),
    path('cars/filter/year/<max_year>/', CarListByYear.as_view(), name='list-cars-by-max-year'),
    path('cars/filter/year/-<min_year>/<max_year>/', CarListByYear.as_view(), name='list-cars-by-year'),
    
    path('auth/login/', ObtainAuthToken.as_view()),
    path('auth/register/', UserCreate.as_view(), name='account-create'),
]