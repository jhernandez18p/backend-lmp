from django.contrib.auth import views as auth_views
from django.urls import path, re_path, include

from .views import custom_login,custom_logout,custom_register, \
    ActivateAccountView, modal_cookie, error, thanks, newsletter,\
    activate, current_user, UserList

app_name = 'auth'
urlpatterns = [
    path('modal', modal_cookie, name='modal-cookie'),
    path('error', error, name='error'),
    path('newsletter', newsletter, name='newsletter'),
    path('gracias', thanks, name='thanks'),
    path('login/', custom_login, name='login'),
    path('salir/', custom_logout, name='logout'),
    path('registro/', custom_register, name='register'),
    path('password_reset/done/', auth_views.password_reset_done, 
        name='password_reset_done'
    ),
    path('password_reset_complete/done/', auth_views.password_reset_complete, 
        name='password_reset_complete'
    ),
    path('password_reset/', auth_views.password_reset, {
        'post_reset_redirect':'auth:password_reset_done',}, name='password_reset'
    ),
    re_path(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, 
        {
            'post_reset_redirect':'auth:password_reset_complete'
        },
        name='password_reset_confirm'
    ),
    re_path(r'^activar-cuenta/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        ActivateAccountView.as_view(), name='activate_account'
    ),
    re_path(r'^activar/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'
    ),
    
    # JWT
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
    
]