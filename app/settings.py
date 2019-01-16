import os
from decouple import config
from django.contrib.messages import constants as message_constants

SITE_ID = 1
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)
ROOT_URLCONF = 'app.urls'
WSGI_APPLICATION = 'app.wsgi.application'
LANGUAGE_CODE = 'es-PA'
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.join(BASE_DIR), 'media')
STATIC_URL = '/static/'
if config('STATIC_ROOT', cast=bool) == True:
    STATIC_ROOT = os.path.abspath(os.path.join(os.path.join(BASE_DIR), 'staticfiles'))
else:
    STATICFILES_DIRS = (os.path.abspath(os.path.join(os.path.join(BASE_DIR), 'staticfiles')),)

MESSAGE_TAGS = {
    message_constants.DEBUG: 'info',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'danger',
}

if DEBUG:
    # DEBUG = True
    ALLOWED_HOSTS = ['*']
    CORS_ORIGIN_ALLOW_ALL = True
    # EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    MESSAGE_LEVEL = message_constants.DEBUG

else:
    # DEBUG = False
    ALLOWED_HOSTS = ['*']
    
    CORS_ORIGIN_WHITELIST = (
        'localhost:9000',
        'localhost:3000',
    )
    MESSAGE_LEVEL = message_constants.INFO

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_TO_USER = EMAIL_HOST_USER

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
    'src.base',
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
    'widget_tweaks',
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


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app.custom_context_processors.brands',
                'app.custom_context_processors.top_cars',
                'app.custom_context_processors.site',
            ],
        },
    },
]

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

AUTHENTICATION_BACKENDS = [
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
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}


JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'src.users.tokens.my_jwt_response_handler'
}

IMPORT_EXPORT_USE_TRANSACTIONS = True
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source']
        ]
    }
}
GOOGLE_RECAPTCHA_SECRET_KEY = config('GOOGLE_SECRET_KEY')