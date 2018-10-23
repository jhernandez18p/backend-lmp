from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.serializers import UserSerializer, BrandSerializer, CarSerializer

from src.cars.models import Car
from src.brands.models import Brand


class UserCreate(APIView):
    """ 
    Creates the user. 
    """

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarListByBrand(generics.ListAPIView):
    serializer_class = CarSerializer

    def get_queryset(self):
        """
            Car filter by Brand
        """
        queryset = Car.objects.all()
        query_brand = self.request.parser_context['kwargs']['slug']
        # print(query_brand)
        
        if query_brand is not None:
            brand = Brand.objects.all()
            for x in brand:
                if x.name.lower() == query_brand.lower():
                    _brand = x
                    # print(_brand.id)
            queryset = queryset.filter(brand_id=_brand.id)
        return queryset


class CarListByModel(generics.ListAPIView):
    serializer_class = CarSerializer

    def get_queryset(self):
        """
            Car filter by Model
        """
        queryset = Car.objects.all()
        query_model = self.request.parser_context['kwargs']['slug']
        # print(query_model)
        
        if query_model is not None:
            queryset = queryset.filter(slug=query_model)
            
        return queryset



class CarListByPrice(generics.ListAPIView):
    serializer_class = CarSerializer

    def get_queryset(self):
        """
        Car filter by price
        """
        queryset = Car.objects.all()
        query_price = self.request.parser_context
        # print(query_price)

        if 'min_price' in query_price['kwargs'] and 'max_price' in query_price['kwargs']:
            print('max_price', 'min_price')
            min_price = query_price['kwargs']['min_price']
            max_price = query_price['kwargs']['max_price']
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        elif 'max_price' in query_price['kwargs']:
            print('max_price')
            price = query_price['kwargs']['max_price']
            queryset = queryset.filter(price__lte=price)

        else:
            # print('min_price')
            price = query_price['kwargs']['min_price']
            queryset = queryset.filter(price__gte=price)

        return queryset


class CarListByYear(generics.ListAPIView):
    serializer_class = CarSerializer

    def get_queryset(self):
        """
        Car filter by year
        """
        queryset = Car.objects.all()
        query_year = self.request.parser_context
        # print(query_year)

        if 'min_year' in query_year['kwargs'] and 'max_year' in query_year['kwargs']:
            print('max_year', 'min_year')
            min_year = query_year['kwargs']['min_year']
            max_year = query_year['kwargs']['max_year']
            queryset = queryset.filter(year__gte=min_year, year__lte=max_year)

        elif 'max_year' in query_year['kwargs']:
            print('max_year')
            year = query_year['kwargs']['max_year']
            queryset = queryset.filter(year__lte=year)

        else:
            # print('min_year')
            year = query_year['kwargs']['min_year']
            queryset = queryset.filter(year__gte=year)

        return queryset

