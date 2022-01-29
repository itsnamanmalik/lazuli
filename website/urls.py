from django.urls import path,include
from website.views import *

urlpatterns = [
        path('', Index.as_view,name="index"),
]