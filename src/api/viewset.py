from django.contrib.sites.models import Site
from django.contrib.auth.models import User

from rest_framework import viewsets

from src.api.serializers import UserSerializer, CarSerializer, BrandSerializer,\
    SiteSerializer, PhotoSerializer, VideoSerializer, ProfileSerializer

from src.cars.models import Car
from src.brands.models import Brand
from src.medias.models import Photo, Video
from src.users.models import Profile


class UserViewSet(viewsets.ModelViewSet):
    """
        User API endpoint
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """
        Profile API endpoint
    """
    queryset = Profile.objects.all().order_by('user_id')
    serializer_class = ProfileSerializer


class CarViewSet(viewsets.ModelViewSet):
    """
        Car API endpoint
    """
    queryset = Car.objects.all().order_by('brand')
    serializer_class = CarSerializer


class BrandViewSet(viewsets.ModelViewSet):
    """
        Brand API endpoint
    """
    queryset = Brand.objects.all().order_by('name')
    serializer_class = BrandSerializer


class SiteViewSet(viewsets.ModelViewSet):
    """
        Site API endpoint
    """
    queryset = Site.objects.all()
    serializer_class = SiteSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    """
        Photo API endpoint
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class VideoViewSet(viewsets.ModelViewSet):
    """
        Video API endpoint
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
