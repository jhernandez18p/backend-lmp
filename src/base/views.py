from urllib.parse import unquote

from django.contrib.sessions.backends.db import SessionStore
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView

from src.cars.models import Car
from src.brands.models import Brand
from src.base.models import Position, Pages, Carousel, CarouselImage
from src.medias.models import Photo, Video

 
class Home(ListView):
    queryset = ''
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            home_page = Pages.objects.get(name='Inicio')

            try:
                header_position = Position.objects.get(name='header')

                try:
                    carousel = Carousel.objects.get(page__name=home_page.name, position__name=header_position.name)

                    if CarouselImage.objects.all().filter(Carousel=carousel.id).count() >= 1:
                        carousel_images = CarouselImage.objects.all().filter(Carousel=carousel.id)
                        context['carousel_image_list'] = carousel_images
                    
                    else:
                        print('No hay imágenes')

                except:
                    print('Carrousel No existe')
            
            except:
                print('Position No existe')
        
        except:
            print('Pages No existe')
        
        object_list = Car.objects.all()
        if object_list.exists():
            context['object_list'] = object_list[:6]

        context['has_newsletter'] = True
        context['title'] = 'Inicio'
        context['SITE_URL'] = 'Inicio'
        context['url'] = reverse('front:home')
        context['menu'] = 'home'
        
        return context


class About(ListView):
    queryset = ''
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            home_page = Pages.objects.get(name='¿Quienes somos?')

            try:
                header_position = Position.objects.get(name='header')

                try:
                    carousel = Carousel.objects.get(page__name=home_page.name, position__name=header_position.name)

                    if CarouselImage.objects.all().filter(Carousel=carousel.id).count() >= 1:
                        carousel_images = CarouselImage.objects.all().filter(Carousel=carousel.id)
                        context['carousel_image_list'] = carousel_images
                    
                    else:
                        print('No hay imágenes')

                except:
                    print('Carrousel No existe')
            
            except:
                print('Position No existe')
        
        except:
            print('Pages No existe')


        context['has_newsletter'] = True
        context['title'] = '¿Quienes somos?'
        context['SITE_URL'] = '¿Quienes somos?'
        context['url'] = reverse('front:about')
        context['menu'] = 'about'
        
        return context


class Inventory(ListView):
    model = Car
    template_name = 'pages/inventory.html'
    paginate_by = 20

    def get_queryset(self):

        object_list = self.model.objects.all()

        price_lower = ''
        if self.request.GET.get('price_lower'):
            price_lower = int(self.request.GET.get('price_lower'))
            object_list = object_list.filter(price__lte=price_lower)
        
        price_higher = ''
        if self.request.GET.get('price_higher'):
            price_higher = int(self.request.GET.get('price_higher'))
            object_list = object_list.filter(price__gte=price_higher)

        year_lower = ''
        if self.request.GET.get('year_lower'):
            line = int(self.request.GET.get('year_lower'))
            object_list = object_list.filter(year__lte=year_lower)
        
        year_higher = ''
        if self.request.GET.get('year_higher'):
            line = int(self.request.GET.get('year_higher'))
            object_list = object_list.filter(year__gte=year_higher)

        brand = ''
        if self.request.GET.get('brand'):
            brand = int(self.request.GET.get('brand'))
            object_list = object_list.filter(brand=brand)

        model = ''
        if self.request.GET.get('model'):
            model = unquote(self.request.GET.get('model'))
            object_list = object_list.filter(model=model)

        search = ''
        if self.request.GET.get('search'):
            search = self.request.GET.get('search')
            object_list = object_list.filter(Q(brand__name__icontains=search)|Q(model__icontains=search)|Q(description__icontains=search))
        
        return object_list

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        price_lower = ''
        if self.request.GET.get('price_lower'):
            price_lower = int(self.request.GET.get('price_lower'))
        
        price_higher = ''
        if self.request.GET.get('price_higher'):
            price_higher = int(self.request.GET.get('price_higher'))

        year_lower = ''
        if self.request.GET.get('year_lower'):
            year_lower = int(self.request.GET.get('year_lower'))
        
        year_higher = ''
        if self.request.GET.get('year_higher'):
            year_higher = int(self.request.GET.get('year_higher'))

        brand = ''
        if self.request.GET.get('brand'):
            brand = Brand.objects.filter(id=int(self.request.GET.get('brand')))[0].name

        model = ''
        if self.request.GET.get('model'):
            model = unquote(self.request.GET.get('model'))

        search = ''
        if self.request.GET.get('search'):
            search = self.request.GET.get('search')
        
        if price_higher == '':
            context['price_higher'] = self.model.objects.all().order_by('price').first().price
        else:
            context['price_higher'] = price_higher
        
        if price_lower == '':
            context['price_lower'] = self.model.objects.all().order_by('-price').first().price
        else:
            context['price_lower'] = price_lower

        if year_higher == '':
            context['year_higher'] = self.model.objects.all().order_by('year').first().year
        else:
            context['year_higher'] = year_higher

        if year_lower == '':
            context['year_lower'] = self.model.objects.all().order_by('-year').first().year
        else:
            context['year_lower'] = year_lower

        context['brand'] = brand
        context['model'] = model
        context['search'] = search

        context['has_newsletter'] = False
        context['SITE_URL'] = 'Inventario'
        context['title'] = 'Inventario'
        context['url'] = reverse('front:inventory')
        context['url_nav'] = 'inventario'
        context['menu'] = 'inventory'

        return context


class CarDetail(DetailView):
    model = Car
    template_name = 'pages/detail/car.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        object_list = self.model.objects.filter(Q(brand=context['object'].brand) | Q(year=context['object'].year)).order_by('?')
        if object_list.exists():
            context['object_list'] = object_list[:4]

        context['object'].update_counter()

        try:
            context['img_list'] = Photo.objects.all().filter(object_id=context['object'].id)
        except:
            print('No hay fotos')

        # form = self.form_class
        # context['form'] = form
        context['has_newsletter'] = False
        context['title'] = 'Detalles: %s %s' %(str(context['object'].brand).capitalize(),str(context['object'].model).capitalize())
        context['url_nav'] = 'productos'
        context['url'] = reverse('front:inventory')
        context['url_nav'] = 'inventario'
        context['menu'] = 'inventory'
        return context



def contact(request):
    if request.method == 'POST':
        if request.POST.get('model'):
            model = request.POST.get('model')
        else:
            model = ''

        if request.POST.get('brand'):
            brand = request.POST.get('brand')
        else:
            brand = ''

        if request.POST.get('name'):
            name = request.POST.get('name')
        else:
            name = ''

        if request.POST.get('email'):
            email = request.POST.get('email')
        else:
            email = ''

        if request.POST.get('phone'):
            phone = request.POST.get('phone')
        else:
            phone = ''

        if request.POST.get('contact'):
            contact = request.POST.get('contact')
        else:
            contact = ''

        if request.POST.get('message'):
            message = request.POST.get('message')
        else:
            message = ''

        if email == '' or name == '':
            return render(request, 'pages/contact.html', {'title': 'Contacto', 'menu':'contact','has_newsletter': True})
        else:
            has_car = ''
            if model != '' and brand != '':
                model_html = '<p>Modelo: %s</p>' % (model)

                brand_html = '<p>Marca: %s</p>' % (brand)

                has_car = '<p>Se encuentra interesado en el vehiculo</p>\n%s \n%s' % (model_html, brand_html)
            
            body_html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta http-equiv="X-UA-Compatible" content="ie=edge">
                <title>Document</title>
            </head>
            <body>
                <h3>Contacto desde la pagina web Luxury Motors Panamá</h3>
                <p>%s ha intentado comunicarse</p>
                <p>Por favor contacatar al:</p>
                <p>Email:%s</p>
                <p>Telefono:%s</p>
                %s
                <p>Nos ha dejado el siguente comentario: </p>
                <p>%s</p>
            </body>
            </html>
            """ % (name, email, phone, has_car, message)

            subject = 'Contacto página web'
            from_email = email
            to = ['luxurymotorspanama@gmail.com']
            text_content = 'Contacto página web'
            html_content = body_html
            
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            subject = 'Mensaje enviado'
            from_email = 'luxurymotorsweb@gmail.com'
            to = [email]
            text_content = 'Contacto página web'
            html_content = 'Gracias %s por contactarnos, en breve nos comunicaremos con ud.' % (name)
            
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return render(request, 'pages/contact.html', {'title': 'Contacto', 'menu':'contact','has_newsletter': True})
        
        return render(request, 'pages/contact.html', {'title': 'Contacto', 'menu':'contact','has_newsletter': True})
    
    else:
        return render(request, 'pages/contact.html', {'title': 'Contacto', 'menu':'contact','has_newsletter': True})
    
    return render(request, 'pages/contact.html', {'title': 'Contacto', 'menu':'contact','has_newsletter': True})
    

def quotations(request):
    if request.GET.get('model'):
        model = request.GET.get('model')
    else:
        model = ''

    if request.GET.get('brand'):
        brand = request.GET.get('brand')
    else:
        brand = ''

    return render(request, 'pages/detail/quotation.html', {
        'title': 'Contacto',
        'menu':'contact',
        'has_newsletter': False,
        'model': model,
        'brand': brand,
    })

def faq(request):
    return render(request, 'pages/detail/faq.html', {'title': 'Contacto', 'menu':'contact','has_newsletter': False})

def booking(request):
    return render(request, 'base/modal.html', {'title': 'Contacto', 'menu':'contact','has_newsletter': False})

def trade_in(request):
    return render(request, 'base/modal.html', {'title': 'Contacto', 'menu':'contact','has_newsletter': False})


''' 
Custom errors
'''
def page_not_found_view(request):
    return render(request, 'pages/errors/page_not_found_view.html', {'error':'page_not_found_view'})

def error_view(request):
    return render(request, 'pages/errors/error_view.html', {'error':'error_view'}) 

def permission_denied_view(request):
    return render(request, 'pages/errors/permission_denied_view.html', {'error':'permission_denied_view'})

def bad_request_view(request):
    return render(request, 'pages/errors/bad_request_view.html', {'error':'bad_request_view'})
