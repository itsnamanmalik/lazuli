import os
from pathlib import Path
from django.contrib import messages


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#DEV
# STATIC_DIR = os.path.join(BASE_DIR,'static')
#DEV


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3r0o^hf^=rsxt9l+(&%+3u4_-7sz*2)%--)d0vw*hfmu7urynq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['https://*.codvensolutions.com','http://*.codvensolutions.com']


INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'website',
    'api',
    'api.customer_requests',
    'api.common',
    'api.ui',
    'api.affiliate',
    'api.users',
    'api.vendors',
    'api.cashback',
    'import_export',
    'django_cleanup',
    'rangefilter',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lazuli.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
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

WSGI_APPLICATION = 'lazuli.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
 'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lazuli',
        'USER': 'root',
        'PASSWORD': '#BakersBrisk#786BB',
        # 'PASSWORD':'', #DEV
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS':{
            'sql_mode': 'traditional',
            'charset': 'utf8mb4',
            'use_unicode': True
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

DEFAULT_AUTO_FIELD='django.db.models.AutoField' 


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
MEDIA_URL = '/media/'


STATIC_ROOT = os.path.join(BASE_DIR, 'static') #DEPLOY

# DEV
# STATICFILES_DIRS = [
#     STATIC_DIR,
# ]

CORS_ORIGIN_ALLOW_ALL = True

TIME_INPUT_FORMATS = ('%I:%M %p',)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser'
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}


MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}



JAZZMIN_SETTINGS = {
    "site_title": "Lazuli Admin",
    "site_header": "Lazuli",
    "site_brand": "Lazuli",
    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "website/images/common/logo.png",
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,
    # Welcome text on the login screen
    "welcome_sign": "Welcome to the Lazuli Admin",
    # Copyright on the footer
    "copyright": "Lazuli Enterprise Pvt Ltd",
    "user_avatar": "",
    #############
    # User Menu #
    #############
    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"name": "Support", "url": "https://codvensolutions.com/contact/", "new_window": True,"icon":"fas fa-question-circle"},
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    # "hide_apps": [],

    # Hide these models when generating side menu (e.g auth.user)
    # "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["auth","authtoken","customer_requests","vendors","vendors.Vendor","vendors.VendorSale","common","affiliate","ui","users.User","users.UserWalletTransaction"],


    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth.CustomUser": "fas fa-user-tie",
        "auth.Group": "fas fa-users",
        "customer_requests.CashbackRequest":"fas fa-money-bill",
        "customer_requests.WithdrawlRequest":"fas fa-wallet",
        "common.Brand":"fas fa-award",
        "common.Category":"fas fa-list-alt",
        "affiliate.DealsCoupon":"fas fa-tags",
        "affiliate.Product":"fas fa-shopping-cart",
        "affiliate.Store":"fas fa-store",
        "ui.SliderLocation":"fas fa-images",
        "ui.Slider":"fas fa-image",
        "users.User":"fas fa-user",
        "users.UserWalletTransaction":"fas fa-money-check",
        "vendors.Vendor":"fas fa-house-user",
        "vendors.VendorSale":"fas fa-cart-arrow-down",
        "vendors.VedorCommissionsTransaction":"fas fa-receipt",
        "vendors.VedorCommissionsTransaction":"fas fa-receipt",
        "cashback.CashbackLevel":"fas fa-tags"
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    # "show_ui_builder": True,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    # "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    # Add a language dropdown into the admin

}



JAZZMIN_UI_TWEAKS = {
    "brand_colour": "navbar-warning",
    "accent": "accent-warning",
    "navbar": "navbar-warning navbar-light",
    "sidebar_fixed": True,
    "navbar_fixed": True,
    "footer_fixed": True,
    "sidebar": "sidebar-light-warning",
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success"
    },
    "actions_sticky_top": False
}
