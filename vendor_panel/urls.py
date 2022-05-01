from django.urls import path,include
from vendor_panel.views import *

urlpatterns = [
        path('dashboard/', Dashboard.as_view(),name="dashboard"),
        path('', VendorLogin.as_view(),name="vendor-login"),
        
]