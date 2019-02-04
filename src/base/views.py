import threading
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
from src.base.models import Position, Pages, Carousel, CarouselImage, FAQ
from src.medias.models import Photo, Video

from decouple import config
from django.core.mail import EmailMessage


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list, sender, uploaded_file, uploaded_file2, uploaded_file3, uploaded_file4, uploaded_file5):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.sender = sender
        self.uploaded_file = uploaded_file
        self.uploaded_file2 = uploaded_file2
        self.uploaded_file3 = uploaded_file3
        self.uploaded_file4 = uploaded_file4
        self.uploaded_file5 = uploaded_file5
        
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.html_content, self.sender, self.recipient_list)
        msg.content_subtype = 'html'
        if self.uploaded_file != '':
            msg.attach(self.uploaded_file.name, self.uploaded_file.read(), self.uploaded_file.content_type)
        
        if self.uploaded_file2 != '':
            msg.attach(self.uploaded_file2.name, self.uploaded_file2.read(), self.uploaded_file2.content_type)
        
        if self.uploaded_file3 != '':
            msg.attach(self.uploaded_file3.name, self.uploaded_file3.read(), self.uploaded_file3.content_type)
        
        if self.uploaded_file4 != '':
            msg.attach(self.uploaded_file4.name, self.uploaded_file4.read(), self.uploaded_file4.content_type)
        
        if self.uploaded_file5 != '':
            msg.attach(self.uploaded_file5.name, self.uploaded_file5.read(), self.uploaded_file5.content_type)
        
        msg.send()

def send_html_mail(subject, html_content, sender, recipient_list, uploaded_file = '', uploaded_file2 = '', uploaded_file3 = '', uploaded_file4 = '', uploaded_file5 = '' ):
    EmailThread(subject, html_content, recipient_list, sender, uploaded_file, uploaded_file2, uploaded_file3, uploaded_file4, uploaded_file5).start()

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
        
        object_list = Car.objects.all().filter(status='IN').order_by('-views')
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
    paginate_by = 18

    def get_queryset(self):

        object_list = self.model.objects.all()

        price_lower = ''
        try:
            price_lower = int(self.request.GET.get('price_lower'))
            object_list = object_list.filter(price__gte=price_lower)
        except:
            pass
        
        price_higher = ''
        try:
            price_higher = int(self.request.GET.get('price_higher'))
            object_list = object_list.filter(price__lte=price_higher)
        except:
            pass
        
        year_lower = ''
        try:
            year_lower = int(self.request.GET.get('year_lower'))
            object_list = object_list.filter(year__gte=year_lower)
        except:
            pass
        
        year_higher = ''
        try:
            year_higher = int(self.request.GET.get('year_higher'))
            object_list = object_list.filter(year__lte=year_higher)
        except:
            pass
        
        brand = ''
        try:
            brand = int(self.request.GET.get('brand'))
            object_list = object_list.filter(brand=brand)
        except:
            pass
        
        model = ''
        try:
            model = unquote(self.request.GET.get('model'))
            object_list = object_list.filter(model=model)
        except:
            pass
        
        search = ''
        try:
            search = self.request.GET.get('search')
            object_list = object_list.filter(Q(brand__name__icontains=search)|Q(model__icontains=search)|Q(description__icontains=search))
        except:
            pass
        
        
        return object_list.filter(Q(status='IN') | Q(status='SOLD'))

    
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
        context = super().get_context_data(**kwargs)

        # filter(Q(brand=context['object'].brand) | Q(year=context['object'].year)).order_by('?')
        # filter(status='IN')

        if self.model.objects.exclude(id=context['object'].id).filter(Q(brand=context['object'].brand) | Q(year=context['object'].year)).order_by('?').count() >= 4:
            query = self.model.objects.filter(
                    ( Q(status='IN') | Q(status='SOLD') ) &
                    ( Q(brand=context['object'].brand) | Q(year=context['object'].year) )
                ).exclude(id=context['object'].id).order_by('?')[:4]
        else:
            query = self.model.objects.filter(Q(status='IN') | Q(status='SOLD')).exclude(id=context['object'].id).order_by('views')[:4]

        context['object_list'] = query


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


class FAQ(ListView):
    template_name = 'pages/detail/faq.html'
    model = FAQ
    paginate_by = 5
    # return render(request, , {'title': 'Contacto', 'menu':'contact','has_newsletter': False})


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

        try:
            pic1 = request.FILES['pic1']
        except:
            pic1 = ''
        
        try:
            pic2 = request.FILES['pic2']
        except:
            pic2 = ''
        
        try:
            pic3 = request.FILES['pic3']
        except:
            pic3 = ''
        
        try:
            pic4 = request.FILES['pic4']
        except:
            pic4 = ''
        
        try:
            pic5 = request.FILES['pic5']
        except:
            pic5 = ''
        
        if request.POST.get('price'):
            price = request.POST.get('price')
        else:
            price = ''
        
        if request.POST.get('color'):
            color = request.POST.get('color')
        else:
            color = ''
        
        if request.POST.get('millaje'):
            millaje = request.POST.get('millaje')
        else:
            millaje = ''
        
        if request.POST.get('year'):
            year = request.POST.get('year')
        else:
            year = ''
        
        if request.POST.get('dir'):
            _dir = request.POST.get('dir')
        else:
            _dir = ''

        if request.POST.get('work-place'):
            _work = request.POST.get('work-place')
        else:
            _work = ''

        if request.POST.get('date'):
            _date = request.POST.get('date')
        else:
            _date = ''

        if request.POST.get('id'):
            _id = request.POST.get('id')
        else:
            _id = ''



        if email == '' or name == '':
            return render(request, 'pages/contact.html', {'title': 'Contacto', 'menu':'contact','has_newsletter': True})
        else:

            has_car = ''
            if model != '' and brand != '' and _dir == '':
                model_html = '<p>Modelo: %s</p>' % (model)

                brand_html = '<p>Marca: %s</p>' % (brand)

                has_car = '<p>Se encuentra interesado en el vehiculo</p>\n%s \n%s' % (model_html, brand_html)
            
            elif model != '' and brand != '' and _dir != '':
                has_car = """
                    <p>Lugar de trabajo: %s</p>
                    <p>Dirección residencial: %s</p>
                    <p>Cedula o pasaporte: %s</p>
                    <p>Datos del auto</p>
                    <p>Marca: %s</p>
                    <p>Modelo: %s</p>
                    <p>Año: %s</p>
                    <p>Color: %s</p>
                    <p>Kilometraje: %s</p>
                    <p>Precio Requerido: %s</p>
                """ % (_work, _dir, _id, brand, model, year, color, millaje, price)
            
            elif _date != '':
                has_car = '<p>Cita para Trade-in</p><p>Fecha: %s</p>' % (_date)
            
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''
            if result['success']:
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
                to = [config('EMAIL_CONTACT'),]
                text_content = 'Contacto página web'
                html_content = body_html
                
                msg = send_html_mail(subject, html_content, from_email, [to], pic1, pic2, pic3, pic4, pic5)
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()

                subject = 'Mensaje enviado'
                from_email = 'luxurymotorsweb@gmail.com'
                to = [email]
                text_content = 'Contacto página web'
                html_content = 'Gracias %s por contactarnos, en breve nos comunicaremos con ud.' % (name)
                
                msg = send_html_mail(subject, html_content, from_email, [to])
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()
                return render(request, 'pages/thanks.html', {'title': 'Contacto', 'menu':'contact','has_newsletter': True})
        
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

def contact_response(request):
    return render(request, 'base/modal.html', {'title': 'Contacto', 'menu':'contact','has_newsletter': False})

def booking(request):
    return render(request, 'base/modal.html', {'title': 'Contacto', 'menu':'contact','has_newsletter': False})

def trade_in(request):
    return render(request, 'base/modal-tradein.html', {'title': 'Trade-In', 'menu':'trade-in','has_newsletter': False})

def sell(request):
    return render(request, 'base/modal-sell.html', {'title': 'Sell', 'menu':'sell','has_newsletter': False})


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
