from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from src.users.models import Profile
from src.brands.models import Brand
from src.cars.models import Car
from src.medias.models import Photo, Video


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        max_length=32,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
             validated_data['password'])
        return user

    class Meta:
        model = User
        # fields = ('id', 'username', 'email', 'password')
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = '__all__'


class SiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Site
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = '__all__'

