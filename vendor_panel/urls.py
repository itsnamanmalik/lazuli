from django.urls import path,include
from vendor_panel.views import *

urlpatterns = [
        path('dashboard/', Dashboard.as_view(),name="dashboard"),
        path('sales/', Sales.as_view(),name="sales"),
        path('marketing-fee/', MarketingFee.as_view(),name="marketing-fee"),
        path('my-profile/', MyProfile.as_view(),name="my-profile"),
        path('reset-password/', ResetPassword.as_view(),name="reset-password"),
        path('add-sales/', AddSales.as_view(),name="add-sales"),
        path('', VendorLogin.as_view(),name="vendor-login"),
        path('vendor-logout/', Logout.as_view(),name="vendor-logout"),
]