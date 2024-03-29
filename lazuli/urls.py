from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

# handler404 = 'website.views.view_404' 



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('api.urls')),
    path('', include('website.urls')),
    path('vendor-panel/', include('vendor_panel.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)