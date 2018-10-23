from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect


from src.users.models import Profile

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel.objects.get(email=username)
            
            if getattr(user, 'is_active', False) and  user.check_password(password):
                # send_mail(
                #     'User Login',
                #     'Here is the message.',
                #     username,
                #     [username],
                #     fail_silently=False,
                # )
                return user
            else:
                return None
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None