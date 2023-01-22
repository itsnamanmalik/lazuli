from django.urls import path,include
from website.views import *

urlpatterns = [
        path('', Index.as_view(),name="index"),
        path('stores/', Stores.as_view(),name="stores"),
        path('brands/', Brands.as_view(),name="brands"),
        path('deals/', Deals.as_view(),name="deals"),
        path('categories/', Categories.as_view(),name="categories"),
        path('deploy-cashback/', DeployCashback.as_view(),name="deploycash"),
        path('withdraw-cashback/', WithdrawCashback.as_view(),name="withdrawcash"),
        path('login/', Login.as_view(),name="login"),
        path('account/', Account.as_view(), name='account'),

]