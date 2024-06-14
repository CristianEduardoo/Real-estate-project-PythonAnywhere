from pathlib import Path
from environ import Env 
import dj_database_url
import os  # Necesaria para el Login

# Variables Globales
env = Env()
Env.read_env()

ENVIRONMENT = env('ENVIRONMENT', default='production')

# Primero, define la ruta base de tu proyecto.
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Luego, define la ruta completa para el directorio de medios. Para guardar img, pdf, etc...
# MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# También, es buena práctica definir la URL para los archivos de medios.
# Para acceder a los archivos de medios desde el navegador.
MEDIA_URL = "/media/"
# MEDIA_ROOT = "/code/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media") # first


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
if ENVIRONMENT == 'development':
    DEBUG = True
else:
    DEBUG = False

# Solo va mi dominio ;)
ALLOWED_HOSTS = ["*"]

# Application definition "channels",  # Biblioteca para manejar conexiones asíncronas
# Aplicaciones de terceros se recomienda primero en la lista
INSTALLED_APPS = [
    "daphne",  # app instalada para servidor asíncrono
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",  # libreria de tercero, para crear nuestra API => pip install djangorestframework
    "drf_spectacular",  # Herramienta para documentar => pip install drf-spectacular
    "django_extensions",  # Social Media
    "social_django",  # Facebook Social Media
    "api",  # aplicacion creada para la API
    "main",
    "blog",
    "users",
    "chat",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # whitenoise
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",  # Facebook Social Media
]

ROOT_URLCONF = 'BienesRaices.urls'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates")
        ],  # Referenciando a todos los templates del directorio
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",  # <-- Facebook
                "social_django.context_processors.login_redirect",  # <-- Facebook
            ],
        },
    },
]

# =============== BACKENDS - Social Media =============== #
AUTHENTICATION_BACKENDS = (
    "social_core.backends.facebook.FacebookOAuth2",
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

# WSGI => WEB SERVER GATEAWAY INTERFACE => SYNCRONA
WSGI_APPLICATION = "BienesRaices.wsgi.application"

# ASGI => ASYNCHRONOUS SERVER GATEAWAY INTERFACE => ASYNCRONA
ASGI_APPLICATION = "BienesRaices.asgi.application"

# Channels-redis Config
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}

# en lugar de localhost => redis

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DB_LOCALLY = False

if ENVIRONMENT == "development" or DB_LOCALLY == True:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "Real-estate-project",
            "USER": "root",
            "PASSWORD": "",
            "HOST": "localhost",
            "PORT": "3306",
        }
    }
else:
    # DATABASES["default"] = dj_database_url.parse(env("DATABASE_URL"))
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "BienesRaices",
            "USER": "admin",
            "PASSWORD": "123qwe@@",
            "HOST": "db",  # from my docker-compose.yml
            "PORT": "5432",
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

STATIC_URL = '/static/'
# STATIC_ROOT = '/code/static/'


# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"), # first 1
# ]

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =============== LOGIN =============== #
# IMPORTANTE SI ES LOGIN -> REDIRECCIONAMOS. ambas constantes estan relacionadas
LOGIN_REDIRECT_URL = "namespaceraices:main"
LOGIN_URL = "login"  # se redirigirá hacer login, si intenta acceder a una vista protegida sin haber iniciado sesión primero
# Django redirigirá al usuario a la página de inicio de sesión, lo tiene por defecto, solo hay que crear el template


# =============== AUTOESQUEMA => ARCHIVO DE DOCUMENTACIÓN DE LA API =============== #
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # Otros ajustes de Django REST Framework...
}

# Configuraciones por defecto:
SPECTACULAR_SETTINGS = {
    "TITLE": "API-PROPIEDADES",
    "DESCRIPTION": "Lista de propiedades",
    "VERSION": "4.2.10",
    "SERVE_INCLUDE_SCHEMA": False,
}
# despues de incluir el AutoEsquema, generarlo => python3 manage.py spectacular --color --file schema.yml


# =============== Custom User =============== #
AUTH_USER_MODEL = 'users.User'


# =============== Facebook - Social Media =============== #
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")

SOCIAL_AUTH_FACEBOOK_KEY = env("SOCIAL_AUTH_FACEBOOK_KEY")
SOCIAL_AUTH_FACEBOOK_SECRET = env("SOCIAL_AUTH_FACEBOOK_SECRET")
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

# Al final de tu archivo settings.py
WHITENOISE_ROOT = os.path.join(BASE_DIR, "media")
