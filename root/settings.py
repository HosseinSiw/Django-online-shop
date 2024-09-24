from datetime import timedelta
from pathlib import Path
from django.urls import reverse

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-%r_8x7r5eeqv@dhd2_*9=xhy28f@03$++2_1clc(sa_uzal-vz'

DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "users.apps.UsersConfig",  # Custom User Application.
    "store.apps.StoreConfig",  # Store app configuration.
    "cart.apps.CartConfig",  # Cart management app.
    "orders.apps.OrdersConfig",  # Order manager application.
    "payment.apps.PaymentConfig",  # Payment managing application
    "rest_framework",  # Djagno Rest Framework.
    'rest_framework_simplejwt',  # SimpleJWT Login.
    "drf_yasg",  # API Documentation.
    'mail_templated',  # Templated Email sending package.

    'django_filters',  # Filtering third party application
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Custom middlewares
    "middleware.CustomLoggingMiddleware",
    "middleware.AdminLoggingMiddleware",
]

ROOT_URLCONF = 'root.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'root.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.CustomUser'

REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ),
        "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# SMTP4DEV configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp4dev'
EMAIL_PORT = 25
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'admin@admin.com'

# Logging custom middleware configuration
LOGGING_FILE_PATH = "logs/requests.logs"
ADMIN_PANEL_URL = '/admin/'  # Change it for make your application more secure
ADMIN_LOGGING_FILE_PATH = 'logs/admin-logs.logs'

# Zarinpal configs
ZARINPAL_MERCHANT_ID = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"  # Use your own ID here
SANDBOX_MODE = True  # Testing mode enabled
ZARINPAL_SANDBOX = True
SECURE_SSL_REDIRECT = False
ZARINPAL_CALLBACK_URL = 'http://127.0.0.1:8000/payment/verify/'
