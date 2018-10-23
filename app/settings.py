import os
from decouple import config
from django.contrib.messages import constants as message_constants
from django.contrib.messages import constants as messages

SITE_ID = 1

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', cast=bool)

if DEBUG:
    # DEBUG = True
    ALLOWED_HOSTS = ['*']
    CORS_ORIGIN_ALLOW_ALL = True
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    MESSAGE_LEVEL = message_constants.DEBUG
else:
    # DEBUG = False
    ALLOWED_HOSTS = ['localhost:*','luxurymotorspanama.com']
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config('EMAIL_HOST')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
    EMAIL_HOST_USER = config('EMAIL_HOST_USER')
    EMAIL_PORT = config('EMAIL_PORT')
    EMAIL_USE_SSL = config('EMAIL_USE_SSL',cast=bool)
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
    EMAIL_TO_USER = EMAIL_HOST_USER
    
    CORS_ORIGIN_WHITELIST = (
        'localhost:9000',
        'localhost:3000',
    )
    MESSAGE_LEVEL = message_constants.INFO

DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    'django.contrib.redirects',
]

LOCAL_APPS = [
    'src.api',
    'src.brands',
    'src.cars',
    'src.medias',
    'src.users',
]

THIRD_PARTY_APPS = [
    'ckeditor',
    'corsheaders',
    'django_filters',
    'import_export',
    'rest_framework.authtoken',
    'rest_framework',
    'social_django',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_USER_PASSWORD'),
        'PORT': config('DB_PORT'),
        'HOST': config('DB_HOST'),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'es-PA'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(os.path.join(BASE_DIR), 'media')

STATIC_URL = '/static/'

if config('STATIC_ROOT', cast=bool) == True:
    STATIC_ROOT = os.path.abspath(os.path.join(os.path.join(BASE_DIR), 'staticfiles'))
    # print('STATIC_ROOT')
else:
    STATICFILES_DIRS = (os.path.abspath(os.path.join(os.path.join(BASE_DIR), 'staticfiles')),)
    # print('staticfiles')


AUTHENTICATION_BACKENDS = [
#     'social_core.backends.github.GithubOAuth2',
#     'social_core.backends.twitter.TwitterOAuth',
#     'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'app.EmailBackend.EmailBackend',
]

# Django Rest Framework Setup
REST_FRAMEWORK = {
#    'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
#         'rest_framework.permissions.IsAuthenticatedOrReadOnly',
#         'rest_framework.permissions.IsAuthenticated',
#    ),
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#         'rest_framework.authentication.TokenAuthentication',
#         'rest_framework.authentication.SessionAuthentication',
#         'rest_framework.authentication.BasicAuthentication',
#     ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    # 'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    )
}


JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'src.users.tokens.my_jwt_response_handler'
}

MESSAGE_TAGS = {
    messages.DEBUG: 'info',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

IMPORT_EXPORT_USE_TRANSACTIONS = True