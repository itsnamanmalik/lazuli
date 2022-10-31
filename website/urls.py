from django.urls import path,include
from website.views import *

urlpatterns = [
        path('', Index.as_view(),name="index"),
        path('stores/', Stores.as_view(),name="stores"),
        path('brands/', Brands.as_view(),name="brands"),
        path('deals/', Deals.as_view(),name="deals"),
        path('deploy-cashback/', DeployCashback.as_view(),name="deploycash"),
        path('login/', Login.as_view(),name="login"),
]