from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv
from decouple import config
import cloudinary
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------
# SECURITY
# -------------------------
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "election-backend-vmwv.onrender.com",
]

# -------------------------
# INSTALLED APPS
# -------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "corsheaders",
    "cloudinary",
    "cloudinary_storage",
    "drf_spectacular",
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",

    # Local apps
    "accounts",
    "vote",
]

# -------------------------
# MIDDLEWARE
# -------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -------------------------
# URL CONFIG
# -------------------------
ROOT_URLCONF = "election.urls"

# -------------------------
# TEMPLATES
# -------------------------
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

# -------------------------
# CORS + CSRF
# -------------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",                       # Vite local
    "https://election-frontend-blush.vercel.app", # Production frontend
]

CSRF_TRUSTED_ORIGINS = [
    "https://election-frontend-blush.vercel.app",
    "https://election-backend-vmwv.onrender.com",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

WSGI_APPLICATION = "election.wsgi.application"

# -------------------------
# DATABASE (Render)
# -------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL"),
        conn_max_age=600
    )
}

# -------------------------
# CUSTOM USER MODEL
# -------------------------
AUTH_USER_MODEL = "accounts.User"
AUTHENTICATION_BACKENDS = [
    "accounts.auth_backend.NationalIDBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# -------------------------
# JWT SETTINGS
# -------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# -------------------------
# STATIC & MEDIA
# -------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
)
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# -------------------------
# INTERNATIONALIZATION
# -------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"




# from pathlib import Path
# import os
# from datetime import timedelta
# from dotenv import load_dotenv
# import cloudinary
# import dj_database_url 
# load_dotenv()
# from decouple import config


# BASE_DIR = Path(__file__).resolve().parent.parent

# # SECURITY
# SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "your-default-secret-key")

# ALLOWED_HOSTS = ["*"]
# SECRET_KEY = config("SECRET_KEY")
# DEBUG = config("DEBUG", default=True, cast=bool)
# ALLOWED_HOSTS = [
#     "127.0.0.1",
#     "localhost",
#     "election-backend-vmwv.onrender.com",
# ]



# # -------------------------
# # Installed Apps
# # -------------------------
# INSTALLED_APPS = [
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",

#     # Third-party
#     "rest_framework",
#     "corsheaders",
#     "cloudinary",
#     "cloudinary_storage",
#     "drf_yasg",
#     "channels",
#     "drf_spectacular",
#     "rest_framework_simplejwt.token_blacklist",
#     "django_filters",

#     # Local apps
#     "accounts",
#     "vote",
# ]

# MIDDLEWARE = [
#     "corsheaders.middleware.CorsMiddleware",
#     'whitenoise.middleware.WhiteNoiseMiddleware',
#     "django.middleware.common.CommonMiddleware",
#     "django.middleware.security.SecurityMiddleware",
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
#     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# ]

# ROOT_URLCONF = "election.urls"

# TEMPLATES = [
#     {
#         "BACKEND": "django.template.backends.django.DjangoTemplates",
#         "DIRS": [],
#         "APP_DIRS": True,
#         "OPTIONS": {
#             "context_processors": [
#                 "django.template.context_processors.request",
#                 "django.contrib.auth.context_processors.auth",
#                 "django.contrib.messages.context_processors.messages",
#             ],
#         },
#     },
# ]

# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",                  # local dev React
#     "http://127.0.0.1:3000",                  # local dev React
#     "https://election-frontend-blush.vercel.app",  # production frontend
# ]

# CORS_ALLOW_CREDENTIALS = True

# CORS_ALLOW_ALL_HEADERS = True


# WSGI_APPLICATION = "election.wsgi.application"

# # -------------------------
# # Database
# # # -------------------------
# # DATABASES = {
# #     "default": {
# #         "ENGINE": "django.db.backends.sqlite3",
# #         "NAME": BASE_DIR / "db.sqlite3",
# #     }
# # }



# DATABASES = {
#     'default': dj_database_url.config(
#         default=config('DATABASE_URL'),
#         conn_max_age=600
#     )
# }

# # DATABASES = {
# #     'default': dj_database_url.config(
# #         default='postgresql://enoverlab_f9kd_user:lC6jdQpU1s2VY9hC8EjuvoYpp9mgvV7W@dpg-d4te9v56ubrc73ekcqq0-a.oregon-postgres.render.com/enoverlab_f9kd',
# #         conn_max_age=600
# #     )
# # }
# AUTH_USER_MODEL = "accounts.User"
# AUTHENTICATION_BACKENDS = [
#     "accounts.auth_backend.NationalIDBackend",  
#     "django.contrib.auth.backends.ModelBackend",
# ]


# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": (
#         "rest_framework_simplejwt.authentication.JWTAuthentication",
#     ),
#     "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
#     "PAGE_SIZE": 10,
#     "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
#     "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
# }

# # -------------------------
# # JWT
# # -------------------------
# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
#     "ROTATE_REFRESH_TOKENS": True,
#     "BLACKLIST_AFTER_ROTATION": True,
#     "AUTH_HEADER_TYPES": ("Bearer",),
# }

# # -------------------------
# # Password Validators
# # -------------------------
# AUTH_PASSWORD_VALIDATORS = [
#     {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
#     {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
#     {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
#     {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
# ]

# # -------------------------
# # Internationalization
# # -------------------------
# LANGUAGE_CODE = "en-us"
# TIME_ZONE = "UTC"
# USE_I18N = True
# USE_TZ = True

# # -------------------------
# # Static & Media
# # -------------------------
# STATIC_URL = "static/"
# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# cloudinary.config(
#     cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
#     api_key=os.environ.get("CLOUDINARY_API_KEY"),
#     api_secret=os.environ.get("CLOUDINARY_API_SECRET")
# )
# DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"


# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {"hosts": [("127.0.0.1", 6379)]},
#     },
# }

# # -------------------------
# # CORS
# # -------------------------
# CORS_ALLOWED_ORIGINS = ["http://localhost:5173"]
# CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_HEADERS = [
#     "accept",
#     "accept-encoding",
#     "authorization",
#     "content-type",
#     "dnt",
#     "origin",
#     "user-agent",
#     "x-csrftoken",
#     "x-requested-with",
# ]

# # settings.py
# STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles'  # where collectstatic will put files

# # Optional: compress static files
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'





