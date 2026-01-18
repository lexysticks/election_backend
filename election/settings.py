from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv
from decouple import config
import cloudinary

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================
# SECURITY
# ==============================
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "electionbackend-production.up.railway.app",
     
]


SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ==============================
# INSTALLED APPS
# ==============================
INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "cloudinary",
    "cloudinary_storage",
    "drf_spectacular",
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",
    "drf_yasg",

    # Local apps
    "accounts",
    "vote",
]


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",

    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "election.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "election.wsgi.application"

# ==============================
# DATABASE (PostgreSQL with SSL)
# ==============================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("PGDATABASE"),
        "USER": os.environ.get("PGUSER"),
        "PASSWORD": os.environ.get("PGPASSWORD"),
        "HOST": os.environ.get("PGHOST"),
        "PORT": os.environ.get("PGPORT", "5432"),
        "OPTIONS": {
            "sslmode": "require",
        },
    }
}

# ==============================
# AUTHENTICATION
# ==============================
AUTH_USER_MODEL = "accounts.User"
AUTHENTICATION_BACKENDS = [
    "accounts.auth_backend.NationalIDBackend",
    "django.contrib.auth.backends.ModelBackend",
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ==============================
# STATIC & MEDIA (Cloudinary)
# ==============================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
)
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# ==============================
# CACHES (Redis)
# ==============================
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# ==============================
# REST FRAMEWORK
# ==============================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 5,
}

# ==============================
# CORS & CSRF (frontend only)
# ==============================


CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",      # dev frontend
    "https://www.voteng.live",    # production frontend
]
# CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "https://www.voteng.live",
]

CORS_ALLOW_CREDENTIALS = True

# CORS_ALLOW_METHODS = [
#     "DELETE",
#     "GET",
#     "OPTIONS",
#     "PATCH",
#     "POST",
#     "PUT",
# ]

# CORS_ALLOW_HEADERS = [
#     "accept",
#     "accept-encoding",
#     "authorization",
#     "content-type",
#     "origin",
#     "user-agent",
#     "x-csrftoken",
#     "x-requested-with",
# ]

# ==============================
# LANGUAGE / TIME
# ==============================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

