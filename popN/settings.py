"""
Django settings for popN project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '##rkc53uu_3_$gx+vvrc9h0t*yzmw$7h(ze-gd^8%i-3p_k@kr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['community.popn.ml','192.168.29.47', '127.0.0.1']


# Application definition


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'community.apps.CommunityConfig',
    #useradded
    'django.contrib.sites',
    'bootstrap',
    'pwa_webpush',
    'fontawesome',
    'captcha',
    'django_user_agents',
    'tracking_analyzer',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

ROOT_URLCONF = 'popN.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'popN.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_db',
        'USER': 'djangouser',
        'PASSWORD': 'popnsecurepassword',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = '/home/ubuntu/popNData/'
    #os.path.join(BASE_DIR, 'media'),
    

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    '/var/www/static/',
]

#PWA settings

PWA_APP_NAME = 'popN'
PWA_APP_DESCRIPTION = "The open community"
PWA_APP_THEME_COLOR = '#91eef5'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/',
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'

PWA_APP_ICONS = [
    {
        'src': '/static/popNicon.png',
        'sizes': '300x300'
    }
]

PWA_APP_LANG = 'en-US'

# Email setup
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'eventdips.ga'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'no-reply@popn.ml'
EMAIL_HOST_PASSWORD = 'popnpassnoreply'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

#Recaptcha
RECAPTCHA_PUBLIC_KEY = '6LfNLskUAAAAAJ8wFJXXblKm94vMO1cUiEoJ8Frv'
RECAPTCHA_PRIVATE_KEY = '6LfNLskUAAAAAEqM3Vi8fHMZ2w4KM4KLXeKbGiGP'

#push notify
WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": "BKtyQqSmOoIW7NGRFYCok25Hts7JOoFMFaPaT5YJSyeoEm_MPn-v9mYyn2q-d1IhuNCifeV2OVKH1iYfFKYmQj4",
    "VAPID_PRIVATE_KEY":"ePR1uNXX_WWHpCEsoMwfX4QU4IgOfzAl6Vi3AYcAIok",
    "VAPID_ADMIN_EMAIL": "arham@popn.ml"
}


GEOIP_PATH =os.path.join(BASE_DIR, 'geoip/')
