from pathlib import Path
import os
import environ

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hiyqr^jgp&)0%a0o%v%&ru4!)nqx8&r(0h_$m7bg$xtd$p$6rd'

#LA CLE OPENAI
OPENAI_API_KEY = env('OPENAI_API_KEY')# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = []

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

#Configuration nécéssaire pour django-allauth
ACCOUNT_EMAIL_VERIFICATION = "none"  # Pas de vérification par e-mail pour le développement
ACCOUNT_EMAIL_REQUIRED = True  # Demande l'e-mail à l'inscription
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # Authentification par e-mail
ACCOUNT_USERNAME_REQUIRED = False  # Pas de nom d'utilisateur requis
LOGIN_REDIRECT_URL = '/personnel/home/'  # Rediriger après connexion
LOGOUT_REDIRECT_URL = '/'  # Rediriger après déconnexion
ACCOUNT_LOGOUT_ON_GET = True  # Se déconnecter sur GET
SOCIALACCOUNT_AUTO_SIGNUP = True  # S'inscrire automatiquement lors de la connexion via un compte social

#Pour l'envoi de mail 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Remplace par ton serveur SMTP
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'gnine.diarra@esprit.tn'
EMAIL_HOST_PASSWORD = 'fuupeumqyupsmbvd'
DEFAULT_FROM_EMAIL = 'team@HospitalPlus.com'


AUTH_USER_MODEL = 'accounts.CustomUser'

#l'URL de mon serveur Ngrok
ALLOWED_HOSTS = ['b540-196-203-207-178.ngrok-free.app', 'localhost', '127.0.0.1']

"""CORS_ALLOWED_ORIGINS = [
    "https://dfc0-196-203-207-178.ngrok-free.app",
]

CORS_ALLOW_METHODS = ['GET', 'POST']  # Méthodes autorisées

CORS_ALLOW_HEADERS = ['Content-Type']  # En-têtes autorisés
# Application definition"""

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'personnel',
    'accounts',
    'patients',
    'corsheaders',
    'import_export',
    'chatbot'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    
]
SITE_ID = 1


ROOT_URLCONF = 'hospitalweb.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'hospitalweb.wsgi.application'

#Configuration du backend d'authentification
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # Authentification standard
    'allauth.account.auth_backends.AuthenticationBackend',  # Authentification allauth
    'accounts.backends.EmailBackend',
)


SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',  # Utilise OAuth2 pour l'authentification
        'APP': {
            'client_id': '1253204102393193',
            'secret': '8760c69026ac2e18ce4102d5bbff8910',
            'key': ''
        },
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'email',
            'name',
            'first_name',
            'last_name',
            'picture',
            'short_name'
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': lambda request: 'en_US',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v21.0',  # Assurez-vous de spécifier la bonne version de l'API
        'REDIRECT_URI': 'https://b540-196-203-207-178.ngrok-free.app/patients/accounts/facebook/login/callback/',
    }
}


CSRF_TRUSTED_ORIGINS = [
    'https://b540-196-203-207-178.ngrok-free.app',  # HTTPS est requis ici
    #'http://c3e5-197-27-120-89.ngrok-free.app',   # HTTP si nécessaire
]


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/



# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
