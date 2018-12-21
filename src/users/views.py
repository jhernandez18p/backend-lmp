import json
import urllib

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text, force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View, ListView, FormView, TemplateView, RedirectView

from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import SignUpForm,NewsletterForm
from .models import Newsletter
from src.users.models import Profile
from src.users.tokens import account_activation_token
from src.users.utils.libs import newsletter_email, reCAPTCHA
from src.api.serializers import UserSerializer

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.profile.email_confirmed = True
            user.profile.status = 'ACTIVE'
            user.save()
            auth.login(request, user)
            return redirect('intra:home')
        else:
            # user is None or link is invalid
            return render(request, 'auth/invalid.html')

def custom_login(request):
    """  Custom user login  """
    form = AuthenticationForm
    context = {
        'SITE_URL': 'Iniciar Sesión',
        'form_name': 'Inicio de Sesión',
        'form_button': 'Inicar Sesión',
        'form': form,
    }

    if not request.user.is_anonymous:
        return HttpResponseRedirect('/')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        result = reCAPTCHA(request.POST.get('g-recaptcha-response'))

        if not username or not password:
            message = {'level':'error','message': 'Asegurese de introducir los datos solicitados.',}
            context['messages'] = message
            return render(request, "auth/form.html", context)
            
        if result['success']:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    _next = "/auth/gracias"
                    if "next" in request.GET:
                        _next = request.GET["next"]
                    if _next == None or _next == "":
                        _next = "/"
                    return HttpResponseRedirect(_next)
                else:
                    message = {'level':'warning','message': 'Su cuenta no esta activa',}
                    context['messages'] = message
                    return render(request, "auth/form.html", context)
            else:
                #User is None
                message = {
                    'level':'warning',
                    'message': 'Ha ocurrido un error con su nombre de usuario o contraseña,\
                    por favor vuelva a intentarlo.',
                }
                context['messages'] = message
                return render(request, "auth/form.html", context)
        else:
            # Error reCAPTCHA
            message = {
                'level':'warning',
                'message': 'Ha ocurrido un error con la validación de sus datos, por favor \
                vuelva a intentarlo.',
            }
            context['messages'] = message
            return render(request, "auth/form.html", context)

    return render(request, "auth/form.html", context)

def custom_register(request):
    ''' Custom user sugn up. '''
    form = SignUpForm(request.POST)
    context = {}
    context['form'] = form
    context['SITE_URL'] = 'Registrarse'
    context['form_name'] = 'Registro de usuario'
    context['form_button'] = 'Registrarse'
    
    if not request.user.is_anonymous:
        return HttpResponseRedirect('/')

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            useremail = form.cleaned_data.get('useremail')
            password = form.cleaned_data.get('password1')
            result = reCAPTCHA(request.POST.get('g-recaptcha-response'))

            if not username or not password:
                message = {'level':'warning','message': 'Asegúrese de introducir los datos solicitados.'}
                context['messages'] = message
                return render(request, "auth/form.html", context)

            if result['success']:
                try:
                    if User.objects.get(email=useremail):
                        message = {
                            'level':'error',
                            'message': 'Ha ocurrido un error, la dirección de correo que introdujo ya existe.',
                        }
                        context['messages'] = message
                        return render(request, "auth/form.html", context)
                except User.DoesNotExist:
                    form.save()
                    user = auth.authenticate(username = username, password = password)
                    current_site = get_current_site(request)
                    subject = 'Activar cuenta de %s' % (current_site.domain)
                    message = render_to_string('registration/account_activation_email.html', {
                        'user': user,
                        'protocol': 'http',
                        'domain': current_site.domain,
                        'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                        'token': account_activation_token.make_token(user),
                    })
                    user.email_user(subject, message)
                    if user is not None:
                        if user.is_active:
                            auth.login(request, user)
                            _next = "/auth/gracias"
                            if "next" in request.GET:
                                _next = request.GET["next"]
                            if _next == None or _next == "":
                                _next = "/auth/gracias"
                            return HttpResponseRedirect(_next)
                        else:
                            # User is not active
                            message = {
                                'level':'warning',
                                'message': 'Parece que no ha activado su cuenta aún.',
                            }
                            context['messages'] = message
                            return render(request, "auth/form.html", context)
        else:
            message = {
                'level':'error',
                'message': 'Ha ocurrido un error, el nombre de usuario ya existe.',
            }
            context['messages'] = message
            return render(request, "auth/form.html", context)

    return render(request, "auth/form.html", context)

def custom_logout(request):
    auth.logout(request)
    if "next" in request.GET:
        _next = request.GET["next"]
    if _next == None or _next == "":
        _next = "/"
    return HttpResponseRedirect(_next)

def newsletter(request):
    if request.method == 'POST':
        return HttpResponseRedirect('/contacto/error')
    else:
        form_name = request.GET.get('Nombre')
        form_email = request.GET.get('Correo')
        print(request.GET.get('Nombre'))
        print('\n\n')
        print(request.GET.get('Correo'))
        
        a = newsletter_email(
            form_name,
            form_email,
            # form_subject,
            # form_message,
            # form_service,
        )
        if a:
            newsletter = Newsletter.objects.filter(Q(name=form_name) | Q(email=form_email))
            if newsletter:
                Newsletter(name=form_name,email=form_email)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.profile.status = 'ACTIVE'
        user.profile.email_confirmed = True
        user.save()
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/')
    else:
        return render(request, 'auth/error.html')

def modal_cookie(request):
    username = request.GET.get('username', None)
    return JsonResponse(username)

def error(request):
    context = {}
    template = 'auth/error.html'
    context['SITE_URL'] = 'Error'
    return render(request, template, context)

def thanks(request):
    return HttpResponseRedirect('/')


"""
JWT
"""

@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)