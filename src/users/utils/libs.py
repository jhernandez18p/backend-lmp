import urllib
import json

import datetime,math,re,os
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.html import strip_tags

def upload_location(instance, filename, *args, **kwargs):
    try:
        a = instance.__class__.__name__
        print(instance.__class__.objects.all())
    except:
        a = 'frontend'
    return os.path.join('sales/%s/'%(a.lower()), datetime.datetime.now().date().strftime("%Y/%m/%d"), filename)

def reCAPTCHA(recaptcha_response):

    ''' Begin reCAPTCHA validation '''
    recaptcha_response = recaptcha_response
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

    return result

def contact_email(self, *args, **kwargs):

    name = self[0]
    to = self[1]
    to2 = settings.EMAIL_TO_USER
    subject = self[2]
    message = self[3]
    url = self[4]


    from_email = settings.EMAIL_HOST_USER
    text_content = 'Hola %s \nSu mensaje \n \"%s\"\nfue recibido correctamente' % (name, message)
    html_content = loader.render_to_string(
        'app/base/email/contact.html',
        {
            'name':name,
            'email':to,
            'subject':subject,
            'message':message,
            'url':url,
        }
    )
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to,to2])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return True

def passwd_reset_email(self, *args, **kwargs):

    name = self[0]
    to = self[1]
    to2 = settings.EMAIL_TO_USER
    subject = self[2]
    message = self[3]
    url = self[4]


    from_email = settings.EMAIL_HOST_USER
    text_content = 'Hola %s \nSu mensaje \n \"%s\"\nfue recibido correctamente' % (name, message)
    html_content = loader.render_to_string(
        'app/base/email/contact.html',
        {
            'name':name,
            'email':to,
            'subject':subject,
            'message':message,
            'url':url,
        }
    )
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to,to2])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return True

def welcome_email(self, *args, **kwargs):

    name = self[0]
    to = self[1]
    to2 = settings.EMAIL_TO_USER
    subject = self[2]
    message = self[3]
    url = self[4]


    from_email = settings.EMAIL_HOST_USER
    text_content = 'Hola %s \nSu mensaje \n \"%s\"\nfue recibido correctamente' % (name, message)
    html_content = loader.render_to_string(
        'app/base/email/contact.html',
        {
            'name':name,
            'email':to,
            'subject':subject,
            'message':message,
            'url':url,
        }
    )
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to,to2])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return True

def newsletter_email(self, *args, **kwargs):

    name = self[0]
    to = self[1]
    to2 = settings.EMAIL_TO_USER

    subject = ''
    from_email = settings.EMAIL_HOST_USER
    text_content = '%s \nSe ha registrado para recibir las newsletters' % (name)
    html_content = loader.render_to_string(
        'app/base/email/contact.html',
        {
            'name':name,
            'email':to
        }
    )
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to,to2])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return True