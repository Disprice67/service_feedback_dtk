import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'activity:index'

KEYS_LIMIT_TABLE = 18
KEYS_LIMIT_PROJECT = 7


INSTALLED_APPS = [
    'activity.apps.ActivityConfig',
    'users.apps.UsersConfig',
    'core.apps.CoreConfig',
    'email_service.apps.EmailServiceConfig',
    'adfs.apps.AdfsConfig',
    'api.apps.ApiConfig',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'adfs.adfs_middleware.RedirectToLoginMiddleware'
]


ROOT_URLCONF = 'feedback.urls'

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
SAML_DIR = os.path.join(BASE_DIR, 'adfs')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

WSGI_APPLICATION = 'feedback.wsgi.application'


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



LANGUAGE_CODE = "ru"

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False



try:
    from .local_settings import *
except ImportError:
    from .prod_settings import *
