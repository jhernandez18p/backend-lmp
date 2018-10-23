from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Newsletter

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Opcional.', label='Nombre')
    last_name = forms.CharField(max_length=30, required=False, help_text='Opcional.', label='Apellido')
    # birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    email = forms.EmailField(max_length=254, help_text='Requerido.')

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email', 'password1', 'password2',]


class NewsletterForm(forms.ModelForm):
    
    class Meta:
        model = Newsletter
        fields = ('name','email')