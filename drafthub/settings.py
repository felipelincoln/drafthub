import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENVIRONMENT = os.environ.get('ENVIRONMENT')

if ENVIRONMENT == 'production':
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ADMIN_URL = os.environ.get('ADMIN_URL')
    DEBUG = 0
    ALLOWED_HOSTS = ['.herokuapp.com', 'localhost', '127.0.0.1']
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_REFERRER_POLICY = 'origin-when-cross-origin'

elif ENVIRONMENT == 'development':
    SECRET_KEY = '&d3b2mg6&=twp3q*!n9f!1#(zp($j34m5ds=e7v2@+t7m&3z4o' # dev key
    ADMIN_URL = 'admin/'
    DEBUG = 1
    ALLOWED_HOSTS = []
    


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',

    # third parties
    'social_django',

    # our apps
    'drafthub.core.apps.CoreConfig',
    'drafthub.draft.apps.DraftConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'drafthub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'drafthub.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),] # dev
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # prod


# Social auth

SOCIAL_AUTH_POSTGRES_JSONFIELD = True
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.github.GithubOAuth2',
)

SOCIAL_AUTH_GITHUB_KEY = '7d8639e8eff3fd36d459'
SOCIAL_AUTH_GITHUB_SECRET = '01d899bc2f63aa109f73d29229c3cd0cbcc4efb0'
LOGIN_REDIRECT_URL = 'home'


# Auth

LOGIN_URL = 'home'
AUTH_USER_MODEL = 'core.Blog'


# Heroku

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
